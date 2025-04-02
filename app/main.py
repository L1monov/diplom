from fastapi import FastAPI
from .api.endpoints import user, pages, trafic

app = FastAPI()

# Регистрация маршрутов
app.include_router(user.router)
app.include_router(pages.router)
app.include_router(trafic.router)
