import random
import socket
import faker
from app.data.database import ClassTrafic
import asyncio
import random

database = ClassTrafic()
async def generate_random_traffic():
    # Генератор случайных данных
    fake = faker.Faker()

    # Генерируем случайные данные для трафика
    address = socket.inet_ntoa(random.randint(0, 2**32-1).to_bytes(4, byteorder='big'))  # Случайный IP
    packets = random.randint(1, 1000)  # Случайное количество пакетов
    bytes_ = random.randint(500, 100000)  # Случайное количество байт
    tx_packets = random.randint(1, packets)  # Случайное количество переданных пакетов
    tx_bytes = random.randint(1, bytes_ // 2)  # Случайное количество переданных байт
    rx_packets = packets - tx_packets  # Количество полученных пакетов
    rx_bytes = bytes_ - tx_bytes  # Количество полученных байт
    country = fake.country()  # Случайная страна
    city = fake.city()  # Случайный город
    as_number = random.randint(10000, 70000)  # Случайный номер AS
    as_organization = fake.company()  # Случайная организация
    description = fake.sentence()  # Описание трафика

    # Возвращаем сгенерированный трафик в виде словаря
    return {
        "address": address,
        "packets": packets,
        "bytes": bytes_,
        "tx_packets": tx_packets,
        "tx_bytes": tx_bytes,
        "rx_packets": rx_packets,
        "rx_bytes": rx_bytes,
        "country": country,
        "city": city,
        "as_number": as_number,
        "as_organization": as_organization,
        "description": description
    }
async def main():
    while True:
        trafic = await generate_random_traffic()
        await database.add_traffic(traffic=trafic)
        time_sleep = random.uniform(.1, 1)
        print(f"Sleep : {time_sleep}")
        await asyncio.sleep(time_sleep)


if __name__ == '__main__':
    asyncio.run(main())