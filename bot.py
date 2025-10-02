import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import openai

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверим, что токены подтянулись
if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не найден. Проверь .env файл!")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY не найден. Проверь .env файл!")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

openai.api_key = OPENAI_API_KEY

# /start
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Привет! Я бот для учёта финансов.\n\n"
                         "Доступные команды:\n"
                         "📊 /stats – статистика\n"
                         "🧹 /reset – сбросить расходы\n"
                         "💡 /advice – совет по экономии\n"
                         "🔮 /forecast – прогноз расходов\n"
                         "❓ /help – помощь")

# /help
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Доступные команды:\n"
                         "📊 /stats – статистика\n"
                         "🧹 /reset – сбросить расходы\n"
                         "💡 /advice – совет по экономии\n"
                         "🔮 /forecast – прогноз расходов\n"
                         "❓ /help – помощь")

# Хранилище расходов (пока в памяти)
expenses = []

# Добавление расходов (обычные сообщения с суммой)
@dp.message(F.text & ~F.text.startswith("/"))
async def add_expense(message: Message):
    text = message.text
    numbers = [int(s) for s in text.split() if s.isdigit()]
    if numbers:
        amount = numbers[0]
        expenses.append(amount)
        await message.answer(f"✅ Записал трату: {amount}₸")
    else:
        await message.answer("❌ Не понял сумму. Напиши, например: 'Такси 1500'")


# /stats
@dp.message(Command("stats"))
async def stats_cmd(message: Message):
    if not expenses:
        await message.answer("Пока нет расходов 📭")
    else:
        total = sum(expenses)
        await message.answer(f"📊 Всего расходов: {total}₸")

# /reset
@dp.message(Command("reset"))
async def reset_cmd(message: Message):
    expenses.clear()
    await message.answer("🧹 Все расходы сброшены!")

# /advice
@dp.message(Command("advice"))
async def advice_cmd(message: Message):
    if not expenses:
        await message.answer("Сначала добавь расходы, потом дам совет 💡")
        return
    total = sum(expenses)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты финансовый помощник."},
            {"role": "user", "content": f"Я потратил {total} тенге. Дай совет, как экономить деньги."}
        ]
    )
    await message.answer("💡 Совет: " + response.choices[0].message.content)

# /forecast
@dp.message(Command("forecast"))
async def forecast_cmd(message: Message):
    if not expenses:
        await message.answer("Нет данных для прогноза 📭")
        return
    total = sum(expenses)
    avg = total / len(expenses)
    forecast = avg * 30
    await message.answer(f"🔮 Прогноз: если тратишь так же, то за месяц выйдет ~{int(forecast)}₸")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
