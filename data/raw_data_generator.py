import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Настройки генерации
NUM_RECORDS = 5000
start_date = datetime(2023, 1, 1)

# Справочники
clients = [f"ООО Водоканал-{i}" for i in range(1, 50)] + [f"УК ЖилСервис-{i}" for i in range(1, 100)]
products = ["Счетчик воды импульсный", "Датчик давления", "Контроллер телеметрии", "УСПД", "Модем GPRS"]
regions = ["Москва", "Санкт-Петербург", "Екатеринбург", "Казань", "Новосибирск"]
managers = ["Иванов", "Смирнов", "Кузнецов", "Попова"]
statuses = ["Успешно реализовано", "Переговоры", "Отказ", "Ожидание оплаты"]

data = []
for _ in range(NUM_RECORDS):
    date = start_date + timedelta(days=random.randint(0, 1000))
    product = random.choice(products)

    # Логика цен и объемов для опта B2B
    if product in ["УСПД", "Контроллер телеметрии"]:
        price = round(random.uniform(15000, 45000), 2)
        qty = random.randint(1, 20)
    else:
        price = round(random.uniform(1500, 5000), 2)
        qty = random.randint(50, 500)

    data.append({
        "transaction_id": f"TRX-{random.randint(100000, 999999)}",
        "date": date.strftime("%Y-%m-%d"),
        "client_name": random.choice(clients),
        "region": random.choice(regions),
        "manager": random.choice(managers),
        "product": product,
        "quantity": qty,
        "unit_price_rub": price,
        "total_revenue_rub": round(qty * price, 2),
        "status": random.choices(statuses, weights=[0.6, 0.2, 0.1, 0.1])[0]
    })

df = pd.DataFrame(data)
df.to_csv("b2b_telemetry_sales_mock.csv", index=False)
print(f"Сгенерировано {len(df)} записей. Файл сохранен как 'b2b_telemetry_sales_mock.csv'.")
display(df.head())