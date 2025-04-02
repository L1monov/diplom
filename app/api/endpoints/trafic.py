from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.requests import Request
from ...data.database import ClassTrafic
from datetime import datetime
import json

router = APIRouter()
TraficDB = ClassTrafic()

from datetime import datetime




@router.get("/get_trafic", response_class=JSONResponse)
async def trafic(request: Request):
    new_trafic = await TraficDB.get_new_traffic()  # Получаем новый трафик

    # Если у нас есть дата, преобразуем ее в строку
    for traffic in new_trafic:
        if isinstance(traffic['created_at'], datetime):  # если есть поле created_at типа datetime
            traffic['created_at'] = traffic['created_at'].isoformat()  # Преобразуем его в строку

    return JSONResponse(content=new_trafic)  # Отправляем данные в формате JSON
