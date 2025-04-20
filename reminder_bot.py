import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configure le logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Remplir avec ton token
BOT_TOKEN = 'YOUR_BOT_TOKEN'
# Remplir avec ton chat_id
CHAT_ID = 'YOUR_CHAT_ID'

async def start(update: Update, context: CallbackContext) -> None:
    """Envoie un message de démarrage au lancement du bot."""
    await update.message.reply_text('Bot lancé !')

async def reminder_job(context: CallbackContext) -> None:
    """Fonction appelée pour envoyer un message de rappel."""
    await context.bot.send_message(chat_id=CHAT_ID, text="N'oublie pas de prendre ton médicament ! 💊")

async def main() -> None:
    """Démarre le bot et configure le JobQueue."""
    # Créer une instance de l'application
    application = Application.builder().token(BOT_TOKEN).build()

    # Planifie un job (par exemple, dans 10 secondes)
    application.job_queue.run_once(reminder_job, 10, context=CHAT_ID)

    # Ajoute un handler pour la commande /start
    application.add_handler(CommandHandler("start", start))

    # Démarre le bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
