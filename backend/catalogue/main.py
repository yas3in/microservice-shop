import os
import sys
from typing import AsyncGenerator, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.config.config import settings
from backend.config.database import init_db
from backend.catalogue.views import (
    CategoryFrontView,
    BrandFrontView,
    ProductTypeFrontView,
    ProductFrontView,
    CategoryAdminView,
    BrandAdminView,
    ProductTypeAdminView,
    ProductAdminView
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Async database initialization
    await init_db()
    yield


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Catalogue Service",
    version="1.0.0",
    lifespan=lifespan
)

# Register Front Class-Based Routers
app.include_router(CategoryFrontView.register_routes())
app.include_router(BrandFrontView.register_routes())
app.include_router(ProductTypeFrontView.register_routes())
app.include_router(ProductFrontView.register_routes())

# Register Admin Class-Based Routers
app.include_router(CategoryAdminView.register_routes())
app.include_router(BrandAdminView.register_routes())
app.include_router(ProductTypeAdminView.register_routes())
app.include_router(ProductAdminView.register_routes())


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {"status": "ok", "service": "catalogue_service", "debug": settings.DEBUG}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PRODUCT_SERVICE_PORT)

