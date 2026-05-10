from fastapi import FastAPI
from app.api.routes.products import router as products_router
from app.api.routes.orders import router as orders_router
from app.api.routes.sellers import router as sellers_router
from app.api.routes.shipments import router as shipments_router
from app.core.database import Base, engine
from app.models import product, seller,user,order


app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"message": "Backend çalışıyor"}

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(sellers_router)
app.include_router(shipments_router)