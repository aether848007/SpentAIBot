import os
import asyncio
import io
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from dotenv import load_dotenv
from openai import OpenAI
from db import init_db, add_expense, get_all_expenses, clear_expenses, DB_NAME

# --- Загрузка переменных окружения ---
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Инициализация базы ---
init_db()

# --- Категории расходов ---
CATEGORIES = {
    "Еда": [
        "еда", "поел", "поесть", "обед", "ужин", "завтрак",
        "продукты", "кафе", "ресторан", "похавал", "покушал", "перекус",
        "бургер", "пицца", "суши", "роллы", "донер", "дёнер", "шаурма",
        "лагман", "самса", "фастфуд", "кофе", "чай", "напиток", "сок",
        "шаурму", "бургеры", "пельмени", "салат", "бутер", "гамбургер"
    ],
    "Одежда": [
        "одежда", "шопинг", "куртка", "джинсы", "кроссовки",
        "обувь", "футболка", "шмотки", "шмот", "лук", "кофта", "платье",
        "брюки", "рубашка", "юбка", "курточка"
    ],
    "Развлечения": [
        "развлечения", "кино", "театр", "игра", "игры", "концерт",
        "гулял", "киношку", "фильм", "бар", "туса", "вечеринка",
        "караоке", "боулинг", "клуб"
    ],
    "Транспорт": [
        "такси", "автобус", "метро", "бензин", "транспорт",
        "таксичка", "маршрутка", "поездка", "самолёт", "поезд", "трамвай"
    ],
    "Дом": [
        "дом", "квартира", "аренда", "свет", "вода",
        "коммуналка", "жкх", "хата", "ремонт", "интернет", "газ", "мебель"
    ],
    "Другое": []
}

# --- Поиск категории ---
def find_category(text: str):
    text = text.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text:
                return category
    return None

# --- Запрос к ИИ для категории ---
async def ask_ai_for_category(text: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты финансовый помощник. Определи категорию расходов (Еда, Одежда, Развлечения, Транспорт, Дом, Другое)."},
            {"role": "user", "content": f"Категоризируй эту трату: {text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# --- Добавление расходов ---
@dp.message(F.text & ~F.text.startswith("/"))
async def add_expense_handler(message: Message):
    text = message.text
    numbers = [int(s) for s in text.split() if s.isdigit()]
    if not numbers:
        await message.answer("❌ Не понял сумму. Напиши: 'Бургер 3000' или 'Такси 1500'")
        return

    amount = numbers[0]
    category = find_category(text)
    if not category:
        category = await ask_ai_for_category(text)
        if category not in CATEGORIES:
            category = "Другое"

    add_expense(category, amount)
    await message.answer(f"✅ Записал: {category} – {amount}₸")

# --- /stats ---
@dp.message(Command("stats"))
async def stats_cmd(message: Message):
    expenses = get_all_expenses()
    if not expenses:
        await message.answer("📭 Пока нет расходов.")
        return

    category_totals = {}
    total = 0
    for category, amount in expenses:
        category_totals[category] = category_totals.get(category, 0) + amount
        total += amount

    result = "📊 Статистика расходов:\n\n"
    for category, amount in category_totals.items():
        result += f"• {category}: {amount}₸\n"
    result += f"\n💰 Общий расход: {total}₸"

    await message.answer(result)

# --- /advice ---
@dp.message(Command("advice"))
async def advice_cmd(message: Message):
    expenses = get_all_expenses()
    if not expenses:
        await message.answer("📭 У тебя пока нет расходов.")
        return

    category_totals = {}
    total = 0
    for category, amount in expenses:
        category_totals[category] = category_totals.get(category, 0) + amount
        total += amount

    summary = ", ".join([f"{cat}: {amt}₸" for cat, amt in category_totals.items()])
    summary_text = f"Текущие расходы: {summary}. Общая сумма: {total}₸."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты финансовый консультант. Дай короткий, практичный совет по личным финансам."},
            {"role": "user", "content": summary_text}
        ]
    )
    advice = response.choices[0].message.content.strip()
    await message.answer(f"💡 Совет:\n\n{advice}")

# --- /forecast ---
@dp.message(Command("forecast"))
async def forecast_cmd(message: Message):
    expenses = get_all_expenses()
    if not expenses:
        await message.answer("📭 У тебя пока нет расходов, нечего прогнозировать.")
        return

    category_totals = {}
    total = 0
    for category, amount in expenses:
        category_totals[category] = category_totals.get(category, 0) + amount
        total += amount

    summary = ", ".join([f"{cat}: {amt}₸" for cat, amt in category_totals.items()])
    summary_text = f"Текущие расходы: {summary}. Общая сумма: {total}₸."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты финансовый аналитик. Сделай прогноз расходов на следующий месяц и краткий анализ."},
            {"role": "user", "content": summary_text}
        ]
    )
    forecast = response.choices[0].message.content.strip()
    await message.answer(f"📈 Прогноз расходов на следующий месяц:\n\n{forecast}")

# --- Графики и фильтры ---
def get_expenses_by_days(days: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_limit = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    cursor.execute("SELECT category, amount FROM expenses WHERE date >= ?", (date_limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_pie_chart(expenses, title):
    category_totals = {}
    for category, amount in expenses:
        category_totals[category] = category_totals.get(category, 0) + amount
    if not category_totals:
        return None

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140)
    ax.set_title(title)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf

# --- /week ---
@dp.message(Command("week"))
async def week_stats(message: Message):
    expenses = get_expenses_by_days(7)
    if not expenses:
        await message.answer("📭 За последнюю неделю расходов нет.")
        return

    total = sum(amount for _, amount in expenses)
    category_totals = {}
    for category, amount in expenses:
        category_totals[category] = category_totals.get(category, 0) + amount

    text = "📅 Расходы за неделю:\n"
    for cat, amt in category_totals.items():
        text += f"• {cat}: {amt}₸\n"
    text += f"\n💰 Всего: {total}₸"

    chart = generate_pie_chart(expenses, "Расходы за неделю")
    if chart:
        await message.answer_photo(BufferedInputFile(chart.read(), filename="week.png"), caption=text)
    else:
        await message.answer(text)

# --- /month ---
@dp.message(Command("month"))
async def month_stats(message: Message):
    expenses = get_expenses_by_days(30)
    if not expenses:
        await message.answer("📭 За последний месяц расходов нет.")
        return

    total = sum(amount for _, amount in expenses)
    category_totals = {}
    for category, amount in expenses:
        category_totals[category] = category_totals.get(category, 0) + amount

    text = "🗓️ Расходы за месяц:\n"
    for cat, amt in category_totals.items():
        text += f"• {cat}: {amt}₸\n"
    text += f"\n💰 Всего: {total}₸"

    chart = generate_pie_chart(expenses, "Расходы за месяц")
    if chart:
        await message.answer_photo(BufferedInputFile(chart.read(), filename="month.png"), caption=text)
    else:
        await message.answer(text)

# --- /reset ---
@dp.message(Command("reset"))
async def reset_cmd(message: Message):
    clear_expenses()
    await message.answer("🧹 Все расходы сброшены!")

# --- /start ---
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "👋 Привет! Я бот для учёта финансов.\n"
        "Просто напиши трату — например: 'бургер 3000'.\n\n"
        "📊 /stats – общая статистика\n"
        "📅 /week – за неделю\n"
        "🗓️ /month – за месяц\n"
        "💡 /advice – совет от ИИ\n"
        "📈 /forecast – прогноз\n"
        "🧹 /reset – сброс\n"
    )

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
