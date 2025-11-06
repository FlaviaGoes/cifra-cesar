from fastapi import FastAPI
from api import routes_cifra

app = FastAPI(title="Cifra de César", version="1.0")

app.include_router(routes_cifra.router)