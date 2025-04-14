from fastapi import FastAPI
from services import service1, service2, service3

app = FastAPI()

app.include_router(service1.router, prefix="/stub/service1")
app.include_router(service2.router, prefix="/stub/service2")
app.include_router(service3.router, prefix="/stub/service3")