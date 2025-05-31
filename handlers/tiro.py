from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler

# Dados das categorias e subcategorias
categorias = {
    "Animaland": ["Demon Slayer", "Jujutsu Kaisen", "Madoka Magica"],
    "Asialand": ["Naruto", "One Piece", "Bleach"],
    "Cineland": ["Marvel", "DC Comics", "Star Wars"],
    "Arcadeland": ["Street Fighter", "Tekken", "Pokemon"],
    "Musicland": ["K-Pop", "Rock", "Jazz"],
    "Diversiland": ["Random1", "Random2", "Random3"]
}

# Função para enviar as categorias ao usuário com botões
async def tiro_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = []
    for cat in categorias.keys():
        keyboard.append([InlineKeyboardButton(cat, callback_data=f"categoria|{cat}")])

    # Enviando imagem ilustrativa (substitua o URL por um link válido)
    image_url = "https://i.imgur.com/7sGZ6bn.png"  # exemplo de imagem qualquer

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption="Escolha uma categoria para dar seus tiros:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Callback para quando escolher uma categoria
async def categoria_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    _, categoria = query.data.split("|")

    subcats = categorias.get(categoria, [])
    keyboard = [[InlineKeyboardButton(sub, callback_data=f"subcategoria|{categoria}|{sub}")] for sub in subcats]

    await query.edit_message_caption(
        caption=f"Você escolheu *{categoria}*. Agora escolha a subcategoria:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Callback para quando escolher a subcategoria
async def subcategoria_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    _, categoria, subcategoria = query.data.split("|")

    # Aqui você vai buscar os personagens da subcategoria, mas por enquanto, só enviaremos uma mensagem teste.
    # Quando for o momento de integrar com o banco de dados, retornaremos a carta com imagem, nome, rank, etc.

    # Exemplo de mensagem temporária
    mensagem = (
        f"Categoria: *{categoria}*\n"
        f"Subcategoria: *{subcategoria}*\n\n"
        "Aqui aparecerá o personagem sorteado com imagem, nome, raridade e outros detalhes."
    )

    await query.edit_message_text(text=mensagem, parse_mode="Markdown")


