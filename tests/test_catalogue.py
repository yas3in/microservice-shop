from typing import AsyncGenerator
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from backend.config.config import settings
from backend.config.database import init_db
from backend.gateway.network import gateway_network
from backend.catalogue.main import app as catalogue_app
from backend.gateway.main import app as gateway_app


@pytest.fixture(autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    await init_db()
    yield


@pytest.mark.asyncio
async def test_category_front_and_admin_crud() -> None:
    """
    Verifies Category Admin CRUD and Front listing/hierarchy tree.
    """
    transport = ASGITransport(app=catalogue_app)
    admin_headers = {"Authorization": "Bearer dev-mock-token"}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Admin Create Parent Category
        parent_resp = await ac.post(
            "/api/v1/catalogue/admin/categories",
            json={"name": "Electronics", "parent": None},
            headers=admin_headers
        )
        assert parent_resp.status_code == 201
        parent_data = parent_resp.json()
        parent_id = parent_data["id"]

        # 2. Admin Create Child Category
        child_resp = await ac.post(
            "/api/v1/catalogue/admin/categories",
            json={"name": "Laptops", "parent": parent_id},
            headers=admin_headers
        )
        assert child_resp.status_code == 201
        child_data = child_resp.json()
        child_id = child_data["id"]

        # 3. Front List Categories
        list_resp = await ac.get("/api/v1/catalogue/categories")
        assert list_resp.status_code == 200
        cats = list_resp.json()
        assert len(cats) >= 2

        # 4. Front Get Category Tree
        tree_resp = await ac.get("/api/v1/catalogue/categories/tree")
        assert tree_resp.status_code == 200
        tree = tree_resp.json()
        parent_nodes = [node for node in tree if node["id"] == parent_id]
        assert len(parent_nodes) == 1
        assert any(c["id"] == child_id for c in parent_nodes[0]["children"])

        # 5. Admin Update Category
        upd_resp = await ac.put(
            f"/api/v1/catalogue/admin/categories/{child_id}",
            json={"name": "Gaming Laptops"},
            headers=admin_headers
        )
        assert upd_resp.status_code == 200
        assert upd_resp.json()["name"] == "Gaming Laptops"


@pytest.mark.asyncio
async def test_brand_crud() -> None:
    """
    Verifies Brand Admin creation and Front detail.
    """
    transport = ASGITransport(app=catalogue_app)
    admin_headers = {"Authorization": "Bearer dev-mock-token"}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create Brand
        brand_resp = await ac.post(
            "/api/v1/catalogue/admin/brands",
            json={"name": "Apple", "parent": None},
            headers=admin_headers
        )
        assert brand_resp.status_code == 201
        brand_id = brand_resp.json()["id"]

        # Front Get Brand
        get_resp = await ac.get(f"/api/v1/catalogue/brands/{brand_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "Apple"


@pytest.mark.asyncio
async def test_product_lifecycle_with_attributes() -> None:
    """
    Verifies complete product flow: ProductType -> Attributes -> Product -> Attribute Values -> Detail View.
    """
    transport = ASGITransport(app=catalogue_app)
    admin_headers = {"Authorization": "Bearer dev-mock-token"}
    upc_code = f"UPC-{str(uuid.uuid4())[:8]}"

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Create Product Type
        type_resp = await ac.post(
            "/api/v1/catalogue/admin/types",
            json={"title": "Smartphone"},
            headers=admin_headers
        )
        assert type_resp.status_code == 201
        type_id = type_resp.json()["id"]

        # 2. Create Attributes for Type
        attr1_resp = await ac.post(
            "/api/v1/catalogue/admin/types/attributes",
            json={"name": "RAM", "product_type": type_id, "attribute_type": "text"},
            headers=admin_headers
        )
        assert attr1_resp.status_code == 201
        attr1_id = attr1_resp.json()["id"]

        attr2_resp = await ac.post(
            "/api/v1/catalogue/admin/types/attributes",
            json={"name": "Storage", "product_type": type_id, "attribute_type": "text"},
            headers=admin_headers
        )
        assert attr2_resp.status_code == 201
        attr2_id = attr2_resp.json()["id"]

        # 3. Create Category & Brand
        cat_resp = await ac.post(
            "/api/v1/catalogue/admin/categories",
            json={"name": "Phones"},
            headers=admin_headers
        )
        cat_id = cat_resp.json()["id"]

        brand_resp = await ac.post(
            "/api/v1/catalogue/admin/brands",
            json={"name": "Samsung"},
            headers=admin_headers
        )
        brand_id = brand_resp.json()["id"]

        # 4. Create Product with Initial Attributes
        prod_resp = await ac.post(
            "/api/v1/catalogue/admin/products",
            json={
                "upc": upc_code,
                "title": "Galaxy S24 Ultra",
                "description": "Flagship smartphone with AI capabilities.",
                "type": type_id,
                "category": cat_id,
                "brand": brand_id,
                "attributes": [
                    {"product_attribute": attr1_id, "value": "12GB"},
                    {"product_attribute": attr2_id, "value": "512GB"}
                ]
            },
            headers=admin_headers
        )
        assert prod_resp.status_code == 201
        prod_id = prod_resp.json()["id"]

        # 5. Front Get Product Detail (resolves attributes, category, brand, type)
        detail_resp = await ac.get(f"/api/v1/catalogue/products/{prod_id}")
        assert detail_resp.status_code == 200
        detail = detail_resp.json()
        assert detail["title"] == "Galaxy S24 Ultra"
        assert detail["category_name"] == "Phones"
        assert detail["brand_name"] == "Samsung"
        assert detail["type_title"] == "Smartphone"
        assert len(detail["attributes"]) == 2

        # 6. Front Search & Filter Products
        search_resp = await ac.get(f"/api/v1/catalogue/products?search=Galaxy&category_id={cat_id}")
        assert search_resp.status_code == 200
        products = search_resp.json()
        assert any(p["id"] == prod_id for p in products)


@pytest.mark.asyncio
async def test_admin_authorization_enforcement() -> None:
    """
    Verifies that non-admin requests to /admin/ routes are rejected with 401/403 when DEBUG=False.
    """
    settings.DEBUG = False
    transport = ASGITransport(app=catalogue_app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/catalogue/admin/categories", json={"name": "Unauthorized Cat"})
        assert resp.status_code == 401

    settings.DEBUG = True


@pytest.mark.asyncio
async def test_gateway_catalogue_proxy_routing() -> None:
    """
    Verifies Gateway routing to Catalogue service via gateway network manager.
    """
    gateway_network.client = AsyncClient(transport=ASGITransport(app=catalogue_app), base_url="http://catalogue-service:8002")
    try:
        transport = ASGITransport(app=gateway_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            resp = await ac.get("/api/v1/catalogue/categories")
            assert resp.status_code == 200
            assert isinstance(resp.json(), list)
    finally:
        await gateway_network.stop()
