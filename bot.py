# bot.py

import logging
from telegram.ext import ApplicationBuilder
import os

# Importa os handlers (funções que respondem aos comandos)
from handlers.start import start_handler
from handlers.tiro import tiro_handler, categoria_callback_handler
from handlers.inventario import inventario_handler
from handlers.admin import addcarta_handler, removercarta_handler, dartiros_handler, darmoedas_handler
from handlers.doar import doar_handler
from handlers.trocar import trocar_handler

# Configuração de logging para ver os prints do bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    if not TOKEN:
        logger.error("Variável de ambiente TELEGRAM_TOKEN não encontrada!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Registra comandos do bot
    app.add_handler(start_handler)
    app.add_handler(tiro_handler)
    app.add_handler(categoria_callback_handler)
    # REMOVIDO: app.add_handler(subcategoria_callback_handler)
    app.add_handler(inventario_handler)
    app.add_handler(addcarta_handler)
    app.add_handler(removercarta_handler)
    app.add_handler(dartiros_handler)
    app.add_handler(darmoedas_handler)
    app.add_handler(doar_handler)
    app.add_handler(trocar_handler)

    logger.info("Bot iniciado e pronto para uso.")
    app.run_polling()

if __name__ == '__main__':
    main()
