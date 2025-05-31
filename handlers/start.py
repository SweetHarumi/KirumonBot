# handlers/start.py

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import random

# Frases para responder quando o usuário enviar /start
FRASES = [
    "Estou vivo!",
    "Oi! Estou aqui para o gacha!",
    "Bot online e pronto!",
    "Bem-vindo ao Gacha Bot!",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frase = random.choice(FRASES)
    await update.message.reply_text(frase)

# Cria o handler do comando /start que vamos registrar no bot.py
start_handler = CommandHandler('start', start)

