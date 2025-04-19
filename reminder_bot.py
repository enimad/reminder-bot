import asyncio
import os
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

confirmed_today = False

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    global confirmed_today
    if confirmed_today:
        return

    keyboard = [[InlineKeyboardButton("✅ Confirmé", callback_data="confirm")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="Coucou mon amour 💖\nN'oublie pas de prendre ton médicament 💊\nClique sur le bouton quand c’est fait ✨",
        reply_markup=reply_markup
    )

    # Rappel dans 10 minutes si pas confirmé
    context.job_queue.run_once(reminder_loop, 600)

async def reminder_loop(context: ContextTypes.DEFAULT_TYPE):
    global confirmed_today
    if not confirmed_today:
        await send_reminder(context)

async def confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global confirmed_today
    confirmed_today = True
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Bravo mon cœur 💖 Je suis fier de toi ✨")

async def reset_confirmation_daily(app):
    while True:
        now = datetime.now()
        target = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1, hours=22)
        wait_time = (target - now).total_seconds()
        await asyncio.sleep(wait_time)
        global confirmed_today
        confirmed_today = False
        app.job_queue.run_once(send_reminder, 0)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CallbackQueryHandler(confirm_callback))

    # Envoi immédiat pour test
app.job_queue.run_once(send_reminder, 0)


    # Reset tous les jours à 22h
    asyncio.create_task(reset_confirmation_daily(app))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
