import asyncio
from typing import List, Union, Dict

import aiomysql

from app.core.config import DB_LOGIN, DB_PASSWORD, DB_PORT, DB_HOST, DB_NAME
from datetime import datetime, timedelta
class AsyncDataBase:

    def __init__(self):
        self.pool = None

    async def init(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=DB_HOST,
                port=int(DB_PORT),
                user=DB_LOGIN,
                password=DB_PASSWORD,
                db=DB_NAME,
                cursorclass=aiomysql.DictCursor,
            )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def execute_query_for_gpt(self, query: str):
        await self.init()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()
                return result

    async def execute_query(self, query: str, args: tuple = ()) -> Union[None, List]:
        await self.init()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                await conn.commit()
                result = await cursor.fetchall()
                return result

class ClassTrafic(AsyncDataBase):
    async def get_new_traffic(self) -> list:
        # Получаем текущее время
        current_time = datetime.now()
        # Рассчитываем время 5 секунд назад
        five_seconds_ago = current_time - timedelta(seconds=5)

        query = """
        SELECT * FROM traffic_data 
        WHERE created_at >= %s
        """

        # Преобразуем время в строковый формат для сравнения с базой
        formatted_time = five_seconds_ago.strftime('%Y-%m-%d %H:%M:%S')
        args = (formatted_time,)
        result = await self.execute_query(query, args )
        return result
    async def add_traffic(self, traffic: dict):
        query = """
        INSERT INTO traffic_data 
        (address, packets, bytes, tx_packets, tx_bytes, rx_packets, rx_bytes, country, city, as_number, as_organization, description, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """

        args = (
            traffic["address"],
            traffic["packets"],
            traffic["bytes"],
            traffic["tx_packets"],
            traffic["tx_bytes"],
            traffic["rx_packets"],
            traffic["rx_bytes"],
            traffic["country"],
            traffic["city"],
            traffic["as_number"],
            traffic["as_organization"],
            traffic["description"]
        )

        await self.execute_query(query, args)

async def main():
    database = ClassTrafic()
    print(await database.get_new_traffic())

if __name__ == '__main__':
    asyncio.run(main())