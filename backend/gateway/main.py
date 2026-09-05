import os
import sys
from typing import AsyncGenerator, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.config.config import settings
from backend.gateway.network import gateway_network


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Start internal network connection pool
    await gateway_network.start()
    try:
        yield
    finally:
        # Shutdown internal network connections
        await gateway_network.stop()


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - API Gateway (XHTTP)",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for browser communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def gateway_health() -> Dict[str, Any]:
    """
    Health check verifying Gateway and internal service reachability via gateway network manager.
    """
    service_map: Dict[str, str] = {
        "auth_service": settings.AUTH_SERVICE_URL,
        "catalogue_service": settings.CATALOGUE_SERVICE_URL,
    }
    services_status = await gateway_network.check_health(service_map)

    return {
        "gateway": "healthy",
        "debug_mode": settings.DEBUG,
        "services": services_status
    }


# ==========================================
# Gateway Route Handlers - Route to Network Manager
# ==========================================

# Auth Service Routing
@app.api_route("/api/v1/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
async def route_auth(request: Request, path: str) -> Response:
    return await gateway_network.forward_request(request, settings.AUTH_SERVICE_URL)


@app.api_route("/api/v1/auth", methods=["GET", "POST", "OPTIONS"])
async def route_auth_root(request: Request) -> Response:
    return await gateway_network.forward_request(request, settings.AUTH_SERVICE_URL)


# Catalogue Service Routing
@app.api_route("/api/v1/catalogue/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
async def route_catalogue(request: Request, path: str) -> Response:
    return await gateway_network.forward_request(request, settings.CATALOGUE_SERVICE_URL)


@app.api_route("/api/v1/catalogue", methods=["GET", "POST", "OPTIONS"])
async def route_catalogue_root(request: Request) -> Response:
    return await gateway_network.forward_request(request, settings.CATALOGUE_SERVICE_URL)


# Mount frontend static directory if exists
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
if os.path.exists(frontend_dir):
    app.mount("/shop", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.GATEWAY_PORT)
