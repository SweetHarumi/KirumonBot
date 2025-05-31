# handlers/start.py

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Função que será executada quando o usuário digitar /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Olá! Eu sou o bot gacha mágico. Use /tiro para tentar a sorte com as cartas!"
    )

# Handler que será registrado no bot.py
start_handler = CommandHandler("start", start)
