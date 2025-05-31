from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import json
import os

USERS_FILE = 'data/users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

async def trocar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Exemplo simples:
    # /trocar <id_carta1> <quantidade1> <id_carta2> <quantidade2> <@usuario_destino ou id>
    args = context.args
    if len(args) < 5:
        await update.message.reply_text("Uso: /trocar <id_carta1> <quantidade1> <id_carta2> <quantidade2> <@usuario ou id>")
        return

    id_carta1 = args[0]
    try:
        qtd1 = int(args[1])
        qtd2 = int(args[3])
    except ValueError:
        await update.message.reply_text("Quantidades precisam ser números inteiros.")
        return
    id_carta2 = args[2]
    destinatario = args[4]

    if qtd1 <= 0 or qtd2 <= 0:
        await update.message.reply_text("As quantidades devem ser maiores que zero.")
        return

    user1_id = str(update.message.from_user.id)

    # Buscar destinatario_id
    if destinatario.startswith('@'):
        destinatario = destinatario[1:]

    users = load_users()

    destinatario_id = None
    if destinatario.isdigit():
        destinatario_id = destinatario
    else:
        for uid, data in users.items():
            if data.get('username', '').lower() == destinatario.lower():
                destinatario_id = uid
                break

    if destinatario_id is None:
        await update.message.reply_text("Usuário destinatário não encontrado ou ainda não usou o bot.")
        return

    if user1_id == destinatario_id:
        await update.message.reply_text("Você não pode trocar cartas consigo mesmo.")
        return

    # Verificar se user1 tem carta1 qtd1
    if user1_id not in users or 'cartas' not in users[user1_id]:
        await update.message.reply_text("Você não tem cartas para trocar.")
        return

    cartas_user1 = users[user1_id]['cartas']
    if id_carta1 not in cartas_user1 or cartas_user1[id_carta1] < qtd1:
        await update.message.reply_text(f"Você não tem {qtd1} cartas de ID {id_carta1}.")
        return

    # Verificar se destinatário tem carta2 qtd2
    if destinatario_id not in users or 'cartas' not in users[destinatario_id]:
        await update.message.reply_text("O destinatário não tem cartas para trocar.")
        return

    cartas_dest = users[destinatario_id]['cartas']
    if id_carta2 not in cartas_dest or cartas_dest[id_carta2] < qtd2:
        await update.message.reply_text(f"O destinatário não tem {qtd2} cartas de ID {id_carta2}.")
        return

    # Fazer a troca:
    # user1 dá id_carta1 qtd1 e recebe id_carta2 qtd2
    cartas_user1[id_carta1] -= qtd1
    if cartas_user1[id_carta1] <= 0:
        del cartas_user1[id_carta1]

    cartas_dest[id_carta2] -= qtd2
    if cartas_dest[id_carta2] <= 0:
        del cartas_dest[id_carta2]

    cartas_user1[id_carta2] = cartas_user1.get(id_carta2, 0) + qtd2
    cartas_dest[id_carta1] = cartas_dest.get(id_carta1, 0) + qtd1

    # Salvar
    save_users(users)

    await update.message.reply_text(f"Troca concluída entre você e {destinatario}!")

trocar_handler = CommandHandler('trocar', trocar

