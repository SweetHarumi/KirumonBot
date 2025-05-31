# handlers/tiro.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

# Lista das 6 categorias principais
CATEGORIAS = [
    ("Animaland", "animaland"),
    ("Asialand", "asialand"),
    ("Cineland", "cineland"),
    ("Arcadeland", "arcadeland"),
    ("Musicland", "musicland"),
    ("Diversiland", "diversiland"),
]

# /tiro: envia as 6 opções de categorias
async def tiro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text=name, callback_data=f"categoria_{code}")]
        for name, code in CATEGORIAS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 Escolha uma categoria de gacha:", reply_markup=reply_markup)

# Callback ao clicar em uma categoria (irá futuramente exibir as subcategorias)
async def categoria_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    categoria_escolhida = query.data.split("_")[1]
    # Aqui vamos carregar as subcategorias dessa categoria (mock por enquanto)
    subcategorias_mock = {
        "animaland": ["Demon Slayer", "Jujutsu Kaisen", "Madoka Magica"],
        "asialand": ["Tokyo Revengers", "Naruto", "Bleach"],
        "cineland": ["Harry Potter", "Marvel", "Star Wars"],
        "arcadeland": ["Zelda", "Mario", "Sonic"],
        "musicland": ["K-Pop", "Rock", "Jazz"],
        "diversiland": ["Pokémon", "Digimon", "Genshin Impact"]
    }

    lista = subcategorias_mock.get(categoria_escolhida, [])
    keyboard = [
        [InlineKeyboardButton(text=sub, callback_data=f"sub_{categoria_escolhida}_{sub}")]
        for sub in lista
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"📂 Subcategorias de {categoria_escolhida.capitalize()}:",
        reply_markup=reply_markup
    )

# Callback ao clicar em uma subcategoria (vai sortear uma carta - em breve)
async def subcategoria_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # No futuro, aqui será feito o sorteio real com imagem, nome, raridade, etc
    await query.edit_message_text("🃏 Em breve: sorteio da carta!")
    

# Exports para o bot.py
tiro_handler = CommandHandler("tiro", tiro)
categoria_callback_handler = CallbackQueryHandler(categoria_callback, pattern="^categoria_")
subcategoria_callback_handler = CallbackQueryHandler(subcategoria_callback, pattern="^sub_")
