# handlers/tiro.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

# Categorias fixas
CATEGORIAS = [
    ("Animaland", "animaland"),
    ("Asialand", "asialand"),
    ("Cineland", "cineland"),
    ("Arcadeland", "arcadeland"),
    ("Musicland", "musicland"),
    ("Diversiland", "diversiland"),
]

# Subcategorias simuladas para teste (depois serão puxadas do banco de dados)
SUBCATEGORIAS = {
    "animaland": ["Demon Slayer", "Madoka Magica", "Beastars"],
    "asialand": ["Jujutsu Kaisen", "Chainsaw Man"],
    "cineland": ["Matrix", "Harry Potter"],
    "arcadeland": ["Pac-Man", "Street Fighter"],
    "musicland": ["Vocaloid", "K/DA"],
    "diversiland": ["Memes", "Famosos"]
}

# 1️⃣ Comando /tiro
async def tiro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"categoria_{valor}")]
        for name, valor in CATEGORIAS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma categoria:", reply_markup=reply_markup)

# 2️⃣ Quando a pessoa escolhe a categoria
async def categoria_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    categoria = query.data.split("_")[1]
    subcategorias = SUBCATEGORIAS.get(categoria, [])

    keyboard = [
        [InlineKeyboardButton(sub, callback_data=f"subcat_{categoria}_{sub}")]
        for sub in subcategorias
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Subcategorias de {categoria.capitalize()}:", reply_markup=reply_markup)

# 3️⃣ Quando a pessoa escolhe a subcategoria
async def subcategoria_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, categoria, subcat = query.data.split("_", 2)

    # ⚠️ Exemplo simulado de carta (depois vamos puxar de banco)
    carta_exemplo = {
        "nome": "Nezuko Kamado",
        "subcategoria": subcat,
        "raridade": "🥈 Raro",
        "imagem_url": "https://i.imgur.com/Z6xH5Oe.png"
    }

    legenda = f"🎴 {carta_exemplo['nome']}\n📂 {carta_exemplo['subcategoria']}\n🏅 {carta_exemplo['raridade']}"
    await query.message.reply_photo(photo=carta_exemplo["imagem_url"], caption=legenda)

# 📦 Handlers para registrar no bot.py
tiro_handler = CommandHandler("tiro", tiro)
categoria_callback_handler = CallbackQueryHandler(categoria_callback, pattern=r"^categoria_")
subcategoria_callback_handler = CallbackQueryHandler(subcategoria_callback, pattern=r"^subcat_")
