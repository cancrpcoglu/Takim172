from fastapi import FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from app.api.routes.products import router as products_router
from app.api.routes.orders import router as orders_router
from app.api.routes.sellers import router as sellers_router
from app.api.routes.shipments import router as shipments_router
from app.api.routes.users import router as users_router
from app.core.database import Base, engine
from app.models import product, seller,user,order
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from fastapi import FastAPI, Header
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.openapi.models import HTTPBearer
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi

app = FastAPI()

# 1. Sadece bunu kullanıyoruz, en temizi budur.
security = HTTPBearer()

# --- SWAGGER'I DÜZELTEN KISIM ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Benim API",
        version="1.0.0",
        routes=app.routes,
    )

    # Üstteki "Authorize" kutusunun adı "BearerAuth" olsun
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # TÜM endpointleri bu "BearerAuth" kutusuna bağlıyoruz
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# -------------------------------

@app.get("/")
def home():
    return {"message": "Backend çalışıyor"}

# Test endpoint'i (Hata veren api_key_header yerine 'security' kullanıyoruz)
@app.get("/test")
def test_endpoint(token: HTTPAuthorizationCredentials = Depends(security)):
    return {"girdiğin_token": token.credentials}

@app.get("/items/")
def read_items(token: HTTPAuthorizationCredentials = Depends(security)):
    return {"token": token.credentials}
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(sellers_router)
app.include_router(shipments_router)
app.include_router(users_router)