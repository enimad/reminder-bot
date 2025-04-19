import logging
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue
from telegram import Update

# Configure le logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Remplir avec ton token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Remplir avec ton chat_id
CHAT_ID = 'YOUR_CHAT_ID'

def start(update: Update, context: CallbackContext) -> None:
    """Envoie un message de démarrage au lancement du bot."""
    update.message.reply_text('Bot lancé !')

def reminder_job(context: CallbackContext) -> None:
    """Fonction appelée pour envoyer un message de rappel."""
    context.bot.send_message(chat_id=CHAT_ID, text="N'oublie pas de prendre ton médicament ! 💊")

def main():
    """Démarre le bot et configure le JobQueue."""
    updater = Updater(token=BOT_TOKEN, use_context=True)

    # Obtient le JobQueue depuis l'Updater
    job_queue = updater.job_queue

    # Planifie un job (exemple : dans 10 secondes)
    job_queue.run_once(reminder_job, 10, context=CHAT_ID)

    # Ajoute un handler pour la commande /start
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Démarre le bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
