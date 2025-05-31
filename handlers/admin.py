# handlers/admin.py

import json
import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

CARDS_FILE = "data/cards.json"
USERS_FILE = "data/users.json"

# Coloque aqui o ID do admin (você). Você pode usar vários se quiser.
ADMIN_IDS = [123456789]  # ⬅️ Substitua pelo seu ID real

def is_admin(user_id):
    return user_id in ADMIN_IDS

def carregar_json(caminho):
    if not os.path.exists(caminho):
        with open(caminho, "w") as f:
            json.dump({}, f)
    with open(caminho, "r") as f:
        return json.load(f)

def salvar_json(caminho, dados):
    with open(caminho, "w") as f:
        json.dump(dados, f, indent=4)

# /addcarta nome|subcategoria|raridade|emoji
async def addcarta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("Você não tem permissão para usar esse comando.")
        return

    try:
        partes = update.message.text.split(" ", 1)[1].split("|")
        nome, subcategoria, raridade, emoji = [p.strip() for p in partes]

        dados = carregar_json(CARDS_FILE)
        if nome in dados:
            await update.message.reply_text("Já existe uma carta com esse nome.")
            return

        dados[nome] = {
            "subcategoria": subcategoria,
            "raridade": raridade,
            "emoji": emoji
        }

        salvar_json(CARDS_FILE, dados)
        await update.message.reply_text(f"Carta '{nome}' adicionada com sucesso.")
    except:
        await update.message.reply_text("Uso correto: /addcarta nome|subcategoria|raridade|emoji")

# /removercarta nome
async def removercarta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("Você não tem permissão para usar esse comando.")
        return

    try:
        nome = update.message.text.split(" ", 1)[1].strip()
        dados = carregar_json(CARDS_FILE)

        if nome not in dados:
            await update.message.reply_text("Carta não encontrada.")
            return

        del dados[nome]
        salvar_json(CARDS_FILE, dados)
        await update.message.reply_text(f"Carta '{nome}' removida com sucesso.")
    except:
        await update.message.reply_text("Uso correto: /removercarta nome")

# /dartiros user_id quantidade
async def dartiros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("Você não tem permissão para usar esse comando.")
        return

    try:
        _, target_id, quantidade = update.message.text.split()
        target_id = str(int(target_id))
        quantidade = int(quantidade)

        dados = carregar_json(USERS_FILE)
        if target_id not in dados:
            dados[target_id] = {"tiros": 0, "moedas": 0, "cartas": []}

        dados[target_id]["tiros"] += quantidade
        salvar_json(USERS_FILE, dados)
        await update.message.reply_text(f"{quantidade} tiros dados ao usuário {target_id}.")
    except:
        await update.message.reply_text("Uso correto: /dartiros user_id quantidade")

# /darmoedas user_id quantidade
async def darmoedas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("Você não tem permissão para usar esse comando.")
        return

    try:
        _, target_id, quantidade = update.message.text.split()
        target_id = str(int(target_id))
        quantidade = int(quantidade)

        dados = carregar_json(USERS_FILE)
        if target_id not in dados:
            dados[target_id] = {"tiros": 0, "moedas": 0, "cartas": []}

        dados[target_id]["moedas"] += quantidade
        salvar_json(USERS_FILE, dados)
        await update.message.reply_text(f"{quantidade} moedas dadas ao usuário {target_id}.")
    except:
        await update.message.reply_text("Uso correto: /darmoedas user_id quantidade")

# Exportando os handlers
addcarta_handler = CommandHandler("addcarta", addcarta)
removercarta_handler = CommandHandler("removercarta", removercarta)
dartiros_handler = CommandHandler("dartiros", dartiros)
darmoedas_handler = CommandHandler("darmoedas", darmoedas)

