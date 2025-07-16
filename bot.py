from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:5000")

BOT_TOKEN = os.getenv("BOT_TOKEN", "COLE_SEU_TOKEN_AQUI")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    response = requests.post(f"{API_URL}/login", json={"telegram_id": telegram_id})
    if response.status_code == 200:
        data = response.json()
        await update.message.reply_text(f"Seu saldo: R${data['saldo']}
Giros: {data['giros']}")
    else:
        await update.message.reply_text("Você ainda não tem conta no painel. Use uma key para ativar.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()