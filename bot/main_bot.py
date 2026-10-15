# Если запускаешь в Colab, сначала нужно установить библиотеки
# !pip install aiogram nest_asyncio pandas

import asyncio
import sqlite3
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import nest_asyncio

# Позволяет запускать асинхронный код в Jupyter/Colab
nest_asyncio.apply()

# ВСТАВЬ СЮДА ТОКЕН ОТ BOTFATHER
API_TOKEN = 'ТВОЙ_ТОКЕН_СЮДА'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для запроса к БД
def get_sales_summary():
    # Укажи правильный путь к базе, если запускаешь не в папке с файлом
    conn = sqlite3.connect('b2b_telemetry.db') 
    
    query = """
    SELECT 
        COUNT(transaction_id) as total_orders,
        SUM(total_revenue_rub) as total_revenue
    FROM fact_sales
    WHERE status = 'Успешно реализовано'
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    orders = df['total_orders'].iloc[0]
    revenue = df['total_revenue'].iloc[0] / 1000000 # Переводим в миллионы
    
    return f"📊 <b>Сводка по продажам телеметрии:</b>\n\n" \
           f"✅ Успешных отгрузок: <b>{orders:,.0f} шт.</b>\n" \
           f"💰 Общая выручка: <b>{revenue:,.2f} млн руб.</b>"

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я аналитический бот B2B-продаж.\nНапиши /report, чтобы получить сводку.")

# Обработчик команды /report
@dp.message(Command("report"))
async def send_report(message: types.Message):
    report_text = get_sales_summary()
    await message.answer(report_text, parse_mode="HTML")

# Запуск бота
async def main():
    print("Бот запущен! Напиши ему /start в Telegram.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())