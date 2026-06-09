from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

expenses = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введіть витрату у форматі:\n100 продукти"
    )

async def list_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not expenses:
        await update.message.reply_text("Витрат поки немає.")
    else:
        text = "Ваші витрати:\n"
        for amount, category in expenses:
            text += f"{amount} грн - {category}\n"
        await update.message.reply_text(text)

async def sum_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = sum(amount for amount, category in expenses)
    await update.message.reply_text(f"Всього витрачено: {total} грн")

async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        parts = update.message.text.split(maxsplit=1)
        amount = float(parts[0])
        category = parts[1]

        expenses.append((amount, category))

        await update.message.reply_text(
            f"Додано: {amount} грн - {category}"
        )
    except:
        await update.message.reply_text(
            "Приклад: 250 продукти"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("list", list_expenses))
app.add_handler(CommandHandler("sum", sum_expenses))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_expense))

app.run_polling()