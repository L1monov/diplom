import datetime
def is_suspicious(traffic):
    # 1. Проверка на необычный трафик по количеству пакетов и байт
    if traffic['packets'] > 500:  # Например, если пакетов больше 500, это может быть подозрительно
        return True
    if traffic['bytes'] > 50000:  # Например, если передано больше 50000 байт
        return True

    # 2. Проверка на страну (например, нежелательные страны)
    suspicious_countries = ['Russia', 'China', 'Iran']  # Пример нежелательных стран
    if traffic['country'] in suspicious_countries:
        return True

    # 3. Проверка на время запроса
    # Предположим, что нормальный трафик идет в рабочие часы
    current_hour = datetime.datetime.now().hour
    if current_hour < 8 or current_hour > 18:  # Например, трафик в ночное время может быть подозрительным
        return True

    # 4. Проверка на описание трафика (например, если описание пустое или выглядит случайным)
    if not traffic['description'] or len(
            traffic['description'].split()) < 3:  # если описание слишком короткое или пустое
        return True

    # Если ни одно из условий не выполнено, то трафик нормальный
    return False

print(len(traffic_list))
# Пример использования
for traffic in traffic_list:
    if is_suspicious(traffic):
        print(f"Подозрительный трафик: {traffic['address']}")
    else:
        print(f"Нормальный трафик: {traffic['address']}")