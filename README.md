# 💰 FinanceBot — AI Telegram Financial Assistant

**FinanceBot** is a smart Telegram bot that helps you track your **expenses, income, and savings goals**.  
It uses **GPT-4** to understand natural language and automatically categorize your transactions.  
The bot also visualizes your financial data with beautiful charts 📊.

---

## 🚀 Features

- 🧾 **Expense & Income Tracking**  
  Just send messages like:

Burger 3000
Salary 200000
I won money in casino 500000

The bot will automatically understand whether it's an income or an expense.

- 🧠 **AI Categorization**  
If the bot doesn’t recognize a category, it uses GPT-4 to determine it automatically.

- 🎯 **Savings Goals**  
You can naturally type:

I want to buy new headphones for 150000
Planning to save for vacation 500000

The bot will detect your goal and start tracking your progress toward it.

- 📅 **Statistics**
- `/stats` — show all-time statistics  
- `/week` — show last 7 days  
- `/month` — show last 30 days  
- `/forecast` — AI forecast for next month  
- `/advice` — get AI-generated financial advice 💡  

- 📈 **Visual Reports**  
The bot generates **pie charts** showing how you spend your money.

- 🧹 **Data Reset**
- `/reset` — clear all expenses and income

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/finance-bot.git
cd finance-bot

2. Install dependencies

pip install -r requirements.txt

3. Create .env file

In the project root, create a file named .env and add:

TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key

4. Run the bot

python bot.py

🗂️ Project Structure

finance-bot/
│
├── bot.py           # Main Telegram bot logic
├── db.py            # SQLite database and helper functions
├── requirements.txt # Python dependencies
├── .env             # API keys (ignored by git)
└── README.md        # Project description

🧩 Technologies

    Aiogram 3

— Telegram bot framework

OpenAI GPT-4o-mini

— AI categorization and advice

Matplotlib

— charts & visualizations

SQLite3

— database

python-dotenv

    — environment variable management

🌱 Example Usage

Expenses & Income

Burger 3000
Taxi 1500
Salary 200000
Freelance 100000

Savings Goal

I want to buy new headphones for 150000

Commands

/stats     — Overall statistics
/week      — Last 7 days
/month     — Last 30 days
/advice    — AI financial advice
/forecast  — AI expense forecast
/reset     — Clear all data

🧠 Future Ideas

    💬 Inline buttons with quick actions

    📊 Goal progress bars

    📱 Web dashboard for visual analytics

    🔔 Savings reminders

SpentAI
💬 Telegram: @FinancialAI_BOT

⭐ If you like this project — don’t forget to star the repo!
