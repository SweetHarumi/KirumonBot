from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

import json
import os

CARDS_FILE = 'data/cards.json'
USERS_FILE = 'data/users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

async def doar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /doar id_carta quantidade @usuario_ou_id
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Uso correto: /doar <ID_da_carta> <quantidade> <@usuario ou id>")
        return

    carta_id = args[0]
    try:
        quantidade = int(args[1])
    except ValueError:
        await update.message.reply_text("Quantidade precisa ser um número inteiro.")
        return

    if quantidade <= 0:
        await update.message.reply_text("Quantidade precisa ser maior que zero.")
        return

    destinatario = args[2]

    # Pegar IDs do doador e destinatário
    doador_id = str(update.message.from_user.id)

    # tentar converter o destinatário para id numérico se possível
    if destinatario.startswith('@'):
        # se for username, tentar buscar o id — **Telegram API não oferece isso diretamente aqui**
        # Só funciona se o usuário já enviou mensagem pro bot (está no users.json)
        destinatario = destinatario[1:]

    users = load_users()

    # pegar id real do destinatário (se username, buscar no users.json)
    destinatario_id = None
    if destinatario.isdigit():
        destinatario_id = destinatario
    else:
        # procurar username no users.json
        for uid, data in users.items():
            if data.get('username', '').lower() == destinatario.lower():
                destinatario_id = uid
                break

    if destinatario_id is None:
        await update.message.reply_text("Destinatário não encontrado ou ainda não usou o bot.")
        return

    if doador_id == destinatario_id:
        await update.message.reply_text("Você não pode doar cartas para si mesmo.")
        return

    # verificar se doador tem cartas
    if doador_id not in users or 'cartas' not in users[doador_id]:
        await update.message.reply_text("Você não tem nenhuma carta para doar.")
        return

    cartas_doador = users[doador_id]['cartas']

    if carta_id not in cartas_doador or cartas_doador[carta_id] < quantidade:
        await update.message.reply_text(f"Você não tem {quantidade} cartas de ID {carta_id}.")
        return

    # retirar do doador
    cartas_doador[carta_id] -= quantidade
    if cartas_doador[carta_id] <= 0:
        del cartas_doador[carta_id]

    # adicionar ao destinatário
    if destinatario_id not in users:
        users[destinatario_id] = {"cartas": {}, "moedas": 0, "tiros": 0}

    cartas_dest = users[destinatario_id].setdefault('cartas', {})
    cartas_dest[carta_id] = cartas_dest.get(carta_id, 0) + quantidade

    # salvar
    save_users(users)

    await update.message.reply_text(
        f"Você doou {quantidade}x carta(s) ID {carta_id} para {destinatario}."
    )


doar_handler = CommandHandler('doar', doar)

