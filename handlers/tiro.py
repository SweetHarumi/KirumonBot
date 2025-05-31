from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
import json
import os

# Caminho para a imagem fixa do gacha (coloque uma imagem no seu /images chamada gacha_cover.jpg)
GACHA_IMAGE_PATH = 'images/Gacha.jpg'

# Exemplo de categorias fixas
CATEGORIAS = [
    "Animaland",
    "Asialand",
    "Cineland",
    "Arcadeland",
    "Musicland",
    "Diversiland"
]

# Exemplo de subcategorias para cada categoria (você deve ajustar para suas subcategorias reais)
SUBCATEGORIAS = {
    "Animaland": ["Demon Slayer", "Jujutsu Kaisen", "Madoka Magica"],
    "Asialand": ["Anime A", "Anime B", "Anime C"],
    "Cineland": ["Movie X", "Movie Y"],
    "Arcadeland": ["Game 1", "Game 2"],
    "Musicland": ["Band A", "Band B"],
    "Diversiland": ["Random 1", "Random 2"]
}

# Função para criar teclado das categorias
def criar_teclado_categorias():
    keyboard = []
    for cat in CATEGORIAS:
        keyboard.append([InlineKeyboardButton(cat, callback_data=f"cat_{cat}")])
    return InlineKeyboardMarkup(keyboard)

# Função para criar teclado das subcategorias
def criar_teclado_subcategorias(categoria):
    keyboard = []
    for subcat in SUBCATEGORIAS.get(categoria, []):
        keyboard.append([InlineKeyboardButton(subcat, callback_data=f"subcat_{categoria}_{subcat}")])
    # Adicionar botão para voltar às categorias
    keyboard.append([InlineKeyboardButton("⬅ Voltar", callback_data="voltar_categorias")])
    return InlineKeyboardMarkup(keyboard)

# Handler do comando /tiro
def tiro_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    # Envia a imagem fixa com o teclado das categorias
    with open(GACHA_IMAGE_PATH, 'rb') as photo:
        update.message.reply_photo(
            photo=photo,
            caption="Escolha uma categoria:",
            reply_markup=criar_teclado_categorias()
        )

# Handler para callbacks dos botões inline
def categoria_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data

    if data == "voltar_categorias":
        # Edita a mensagem para mostrar categorias e manter a imagem fixa
        query.edit_message_caption(
            caption="Escolha uma categoria:",
            reply_markup=criar_teclado_categorias()
        )
        return

    if data.startswith("cat_"):
        categoria = data[len("cat_"):]
        # Edita a mensagem para mostrar as subcategorias daquela categoria
        query.edit_message_caption(
            caption=f"Categoria: {categoria}\nEscolha uma subcategoria:",
            reply_markup=criar_teclado_subcategorias(categoria)
        )
        return

    # Caso seja subcategoria
    if data.startswith("subcat_"):
        # Extrai categoria e subcategoria
        _, categoria, subcategoria = data.split("_", 2)

        # Aqui você deve implementar a lógica para mostrar a carta final da subcategoria
        # Exemplo: buscar uma carta aleatória daquela subcategoria e enviar foto + texto
        carta = buscar_carta_por_subcategoria(subcategoria)
        if carta:
            foto_path = f"images/{carta['id']}.jpg"  # suposição que a imagem é salva com id da carta
            legenda = (
                f"Nome: {carta['nome']}\n"
                f"Subcategoria: {carta['subcategoria']}\n"
                f"Rank: {rank_para_emoji(carta['raridade'])}"
            )
            # Envia nova mensagem com a carta
            context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=open(foto_path, 'rb'),
                caption=legenda
            )
        else:
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Nenhuma carta encontrada para essa subcategoria."
            )
        return

def buscar_carta_por_subcategoria(subcategoria):
    # Carrega cards.json
    if not os.path.exists('data/cards.json'):
        return None
    with open('data/cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)

    # Filtra cartas da subcategoria
    cartas_subcat = [c for c in cards if c['subcategoria'] == subcategoria]

    if not cartas_subcat:
        return None

    # Retorna uma carta aleatória
    import random
    return random.choice(cartas_subcat)

def rank_para_emoji(raridade):
    # Mapear raridade para emoji medalha
    mapping = {
        "comum": "🥉",
        "raro": "🥈",
        "lendario": "🥇"
    }
    return mapping.get(raridade.lower(), "")

# Handlers para registrar
tiro_handler = CommandHandler('tiro', tiro_handler)
categoria_callback_handler = CallbackQueryHandler(categoria_callback_handler, pattern='^(cat_|subcat_|voltar_categorias)')
