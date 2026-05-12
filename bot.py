import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from mistralai import Mistral

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
MY_NAME = "ЛядовGPT"

client = Mistral(api_key=MISTRAL_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Привет, я {MY_NAME}. Спрашивай!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": f"Ты — {MY_NAME}. Отвечай как человек. Не говори что ИИ. На русском."},
                {"role": "user", "content": user_text}
            ]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("Бот запущен!")
app.run_polling()