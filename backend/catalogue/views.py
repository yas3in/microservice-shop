from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.config.database import get_async_session
from backend.gateway.security import get_current_admin_user_payload
from backend.catalogue.models import (
    Category, CategoryCreate, CategoryUpdate, CategoryRead, CategoryTreeRead,
    Brand, BrandCreate, BrandUpdate, BrandRead,
    ProductType, ProductTypeCreate, ProductTypeUpdate, ProductTypeRead,
    ProductAttribute, ProductAttributeCreate, ProductAttributeUpdate, ProductAttributeRead,
    Product, ProductCreate, ProductUpdate, ProductRead, ProductDetailRead,
    ProductAttributeValue, AttributeValueInput, ProductAttributeValueRead
)


# =====================================================================
# FRONT / PUBLIC CLASS-BASED VIEWS
# =====================================================================

class CategoryFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/categories", tags=["Front - Categories"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[CategoryRead])
        async def list_categories(
            parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Category]:
            stmt = select(Category)
            if parent_id is not None:
                stmt = stmt.where(Category.parent == parent_id)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/tree", response_model=List[CategoryTreeRead])
        async def get_category_tree(
            db: AsyncSession = Depends(get_async_session)
        ) -> List[CategoryTreeRead]:
            stmt = select(Category)
            res = await db.exec(stmt)
            all_categories = list(res.all())

            # Build recursive hierarchy
            category_map: Dict[int, CategoryTreeRead] = {
                c.id: CategoryTreeRead(id=c.id, name=c.name, parent=c.parent, children=[])  # type: ignore
                for c in all_categories if c.id is not None
            }

            tree: List[CategoryTreeRead] = []
            for c in all_categories:
                if c.id is not None:
                    node = category_map[c.id]
                    if c.parent and c.parent in category_map:
                        category_map[c.parent].children.append(node)
                    else:
                        tree.append(node)
            return tree

        @router.get("/{category_id}", response_model=CategoryRead)
        async def get_category(
            category_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> Category:
            stmt = select(Category).where(Category.id == category_id)
            res = await db.exec(stmt)
            category = res.first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
            return category

        return router


class BrandFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/brands", tags=["Front - Brands"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[BrandRead])
        async def list_brands(
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Brand]:
            stmt = select(Brand)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/{brand_id}", response_model=BrandRead)
        async def get_brand(
            brand_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> Brand:
            stmt = select(Brand).where(Brand.id == brand_id)
            res = await db.exec(stmt)
            brand = res.first()
            if not brand:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found.")
            return brand

        return router


class ProductTypeFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/types", tags=["Front - Product Types"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[ProductTypeRead])
        async def list_types(
            db: AsyncSession = Depends(get_async_session)
        ) -> List[ProductType]:
            stmt = select(ProductType)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/{type_id}/attributes", response_model=List[ProductAttributeRead])
        async def list_type_attributes(
            type_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> List[ProductAttribute]:
            stmt = select(ProductAttribute).where(ProductAttribute.product_type == type_id)
            res = await db.exec(stmt)
            return list(res.all())

        return router


class ProductFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/products", tags=["Front - Products"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[ProductRead])
        async def list_products(
            search: Optional[str] = Query(None, description="Search by title or description"),
            category_id: Optional[int] = Query(None, description="Filter by category"),
            brand_id: Optional[int] = Query(None, description="Filter by brand"),
            type_id: Optional[int] = Query(None, description="Filter by product type"),
            limit: int = Query(50, ge=1, le=100),
            offset: int = Query(0, ge=0),
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Product]:
            stmt = select(Product)
            if search:
                stmt = stmt.where(Product.title.ilike(f"%{search}%") | Product.description.ilike(f"%{search}%"))
            if category_id is not None:
                stmt = stmt.where(Product.category == category_id)
            if brand_id is not None:
                stmt = stmt.where(Product.brand == brand_id)
            if type_id is not None:
                stmt = stmt.where(Product.type == type_id)

            stmt = stmt.offset(offset).limit(limit)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/{product_id}", response_model=ProductDetailRead)
        async def get_product_detail(
            product_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductDetailRead:
            stmt = select(Product).where(Product.id == product_id)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            # Resolve Category, Brand, and Type Names
            cat_stmt = select(Category).where(Category.id == product.category)
            cat_res = await db.exec(cat_stmt)
            cat = cat_res.first()

            brand_name = None
            if product.brand:
                brand_stmt = select(Brand).where(Brand.id == product.brand)
                brand_res = await db.exec(brand_stmt)
                b = brand_res.first()
                if b:
                    brand_name = b.name

            type_stmt = select(ProductType).where(ProductType.id == product.type)
            type_res = await db.exec(type_stmt)
            ptype = type_res.first()

            # Resolve Attributes
            val_stmt = select(ProductAttributeValue).where(ProductAttributeValue.product == product.id)
            val_res = await db.exec(val_stmt)
            attr_values = list(val_res.all())

            attr_items: List[ProductAttributeValueRead] = []
            for val in attr_values:
                attr_def_stmt = select(ProductAttribute).where(ProductAttribute.id == val.product_attribute)
                attr_def_res = await db.exec(attr_def_stmt)
                attr_def = attr_def_res.first()
                attr_items.append(ProductAttributeValueRead(
                    id=val.id,  # type: ignore
                    product_attribute=val.product_attribute,
                    attribute_name=attr_def.name if attr_def else None,
                    value=val.value,
                    product=val.product
                ))

            return ProductDetailRead(
                id=product.id,  # type: ignore
                upc=product.upc,
                title=product.title,
                description=product.description,
                type=product.type,
                category=product.category,
                brand=product.brand,
                category_name=cat.name if cat else None,
                brand_name=brand_name,
                type_title=ptype.title if ptype else None,
                attributes=attr_items
            )

        @router.get("/upc/{upc_code}", response_model=ProductDetailRead)
        async def get_product_by_upc(
            upc_code: str,
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductDetailRead:
            stmt = select(Product).where(Product.upc == upc_code)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
            return await get_product_detail(product.id, db)  # type: ignore

        return router


# =====================================================================
# ADMIN CLASS-BASED VIEWS
# =====================================================================

class CategoryAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/categories", tags=["Admin - Categories"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
        async def create_category(
            category_in: CategoryCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Category:
            category = Category(
                name=category_in.name,
                parent=category_in.parent
            )
            db.add(category)
            await db.commit()
            await db.refresh(category)
            return category

        @router.put("/{category_id}", response_model=CategoryRead)
        async def update_category(
            category_id: int,
            category_in: CategoryUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Category:
            stmt = select(Category).where(Category.id == category_id)
            res = await db.exec(stmt)
            category = res.first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

            update_data = category_in.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(category, k, v)

            db.add(category)
            await db.commit()
            await db.refresh(category)
            return category

        @router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_category(
            category_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(Category).where(Category.id == category_id)
            res = await db.exec(stmt)
            category = res.first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

            await db.delete(category)
            await db.commit()
            return None

        return router


class BrandAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/brands", tags=["Admin - Brands"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.post("", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
        async def create_brand(
            brand_in: BrandCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Brand:
            brand = Brand(
                name=brand_in.name,
                parent=brand_in.parent
            )
            db.add(brand)
            await db.commit()
            await db.refresh(brand)
            return brand

        @router.put("/{brand_id}", response_model=BrandRead)
        async def update_brand(
            brand_id: int,
            brand_in: BrandUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Brand:
            stmt = select(Brand).where(Brand.id == brand_id)
            res = await db.exec(stmt)
            brand = res.first()
            if not brand:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found.")

            update_data = brand_in.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(brand, k, v)

            db.add(brand)
            await db.commit()
            await db.refresh(brand)
            return brand

        @router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_brand(
            brand_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(Brand).where(Brand.id == brand_id)
            res = await db.exec(stmt)
            brand = res.first()
            if not brand:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found.")

            await db.delete(brand)
            await db.commit()
            return None

        return router


class ProductTypeAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/types", tags=["Admin - Types & Attributes"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.post("", response_model=ProductTypeRead, status_code=status.HTTP_201_CREATED)
        async def create_type(
            type_in: ProductTypeCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductType:
            ptype = ProductType(title=type_in.title)
            db.add(ptype)
            await db.commit()
            await db.refresh(ptype)
            return ptype

        @router.put("/{type_id}", response_model=ProductTypeRead)
        async def update_type(
            type_id: int,
            type_in: ProductTypeUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductType:
            stmt = select(ProductType).where(ProductType.id == type_id)
            res = await db.exec(stmt)
            ptype = res.first()
            if not ptype:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductType not found.")

            if type_in.title is not None:
                ptype.title = type_in.title

            db.add(ptype)
            await db.commit()
            await db.refresh(ptype)
            return ptype

        @router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_type(
            type_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(ProductType).where(ProductType.id == type_id)
            res = await db.exec(stmt)
            ptype = res.first()
            if not ptype:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductType not found.")

            await db.delete(ptype)
            await db.commit()
            return None

        @router.post("/attributes", response_model=ProductAttributeRead, status_code=status.HTTP_201_CREATED)
        async def create_attribute(
            attr_in: ProductAttributeCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductAttribute:
            attr = ProductAttribute(
                name=attr_in.name,
                product_type=attr_in.product_type,
                attribute_type=attr_in.attribute_type
            )
            db.add(attr)
            await db.commit()
            await db.refresh(attr)
            return attr

        @router.put("/attributes/{attribute_id}", response_model=ProductAttributeRead)
        async def update_attribute(
            attribute_id: int,
            attr_in: ProductAttributeUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductAttribute:
            stmt = select(ProductAttribute).where(ProductAttribute.id == attribute_id)
            res = await db.exec(stmt)
            attr = res.first()
            if not attr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attribute not found.")

            update_data = attr_in.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(attr, k, v)

            db.add(attr)
            await db.commit()
            await db.refresh(attr)
            return attr

        @router.delete("/attributes/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_attribute(
            attribute_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(ProductAttribute).where(ProductAttribute.id == attribute_id)
            res = await db.exec(stmt)
            attr = res.first()
            if not attr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attribute not found.")

            await db.delete(attr)
            await db.commit()
            return None

        return router


class ProductAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/products", tags=["Admin - Products"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
        async def create_product(
            product_in: ProductCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Product:
            # Check unique UPC
            upc_stmt = select(Product).where(Product.upc == product_in.upc)
            upc_res = await db.exec(upc_stmt)
            if upc_res.first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UPC already registered.")

            product = Product(
                upc=product_in.upc,
                title=product_in.title,
                description=product_in.description,
                type=product_in.type,
                category=product_in.category,
                brand=product_in.brand
            )
            db.add(product)
            await db.commit()
            await db.refresh(product)

            # Add optional initial attribute values
            if product_in.attributes:
                for attr_val in product_in.attributes:
                    val_obj = ProductAttributeValue(
                        product_attribute=attr_val.product_attribute,
                        value=attr_val.value,
                        product=product.id  # type: ignore
                    )
                    db.add(val_obj)
                await db.commit()

            return product

        @router.put("/{product_id}", response_model=ProductRead)
        async def update_product(
            product_id: int,
            product_in: ProductUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Product:
            stmt = select(Product).where(Product.id == product_id)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            update_data = product_in.model_dump(exclude_unset=True)
            attributes_data = update_data.pop("attributes", None)

            for k, v in update_data.items():
                setattr(product, k, v)

            db.add(product)
            await db.commit()
            await db.refresh(product)

            # Sync attribute values if specified
            if attributes_data is not None:
                # Delete existing values
                del_stmt = delete(ProductAttributeValue).where(ProductAttributeValue.product == product.id)
                await db.exec(del_stmt)
                for attr_val in attributes_data:
                    val_obj = ProductAttributeValue(
                        product_attribute=attr_val["product_attribute"],
                        value=attr_val["value"],
                        product=product.id  # type: ignore
                    )
                    db.add(val_obj)
                await db.commit()

            return product

        @router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_product(
            product_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(Product).where(Product.id == product_id)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            # Delete attribute values
            del_stmt = delete(ProductAttributeValue).where(ProductAttributeValue.product == product.id)
            await db.exec(del_stmt)

            await db.delete(product)
            await db.commit()
            return None

        @router.post("/{product_id}/attributes", response_model=ProductAttributeValueRead, status_code=status.HTTP_201_CREATED)
        async def set_product_attribute_value(
            product_id: int,
            val_in: AttributeValueInput,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductAttributeValueRead:
            prod_stmt = select(Product).where(Product.id == product_id)
            prod_res = await db.exec(prod_stmt)
            if not prod_res.first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            # Check if attribute already exists for product -> update, else insert
            val_stmt = select(ProductAttributeValue).where(
                ProductAttributeValue.product == product_id,
                ProductAttributeValue.product_attribute == val_in.product_attribute
            )
            val_res = await db.exec(val_stmt)
            existing_val = val_res.first()

            if existing_val:
                existing_val.value = val_in.value
                db.add(existing_val)
                await db.commit()
                await db.refresh(existing_val)
                res_obj = existing_val
            else:
                new_val = ProductAttributeValue(
                    product_attribute=val_in.product_attribute,
                    value=val_in.value,
                    product=product_id
                )
                db.add(new_val)
                await db.commit()
                await db.refresh(new_val)
                res_obj = new_val

            attr_def_stmt = select(ProductAttribute).where(ProductAttribute.id == res_obj.product_attribute)
            attr_def_res = await db.exec(attr_def_stmt)
            attr_def = attr_def_res.first()

            return ProductAttributeValueRead(
                id=res_obj.id,  # type: ignore
                product_attribute=res_obj.product_attribute,
                attribute_name=attr_def.name if attr_def else None,
                value=res_obj.value,
                product=res_obj.product
            )

        return router
