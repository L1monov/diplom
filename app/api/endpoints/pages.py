from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.requests import Request
from ...data.database import ClassTrafic
from datetime import datetime
import json

router = APIRouter()
TraficDB = ClassTrafic()
# Указываем директорию для шаблонов
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Функция для преобразования datetime в строку
def datetime_converter(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Преобразуем datetime в строку ISO 8601
    raise TypeError("Type not serializable")



@router.get("/trafic", response_class=HTMLResponse)
async def trafic(request: Request):
    new_trafic = await TraficDB.get_new_traffic()  # Получаем новый трафик
    return templates.TemplateResponse("trafic.html", {"request": request, "new_trafic": new_trafic})