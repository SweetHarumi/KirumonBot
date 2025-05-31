# handlers/inventario.py

import json
import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

USERS_FILE = "data/users.json"

def carregar_dados_usuarios():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def salvar_dados_usuarios(dados):
    with open(USERS_FILE, "w") as f:
        json.dump(dados, f, indent=4)

def garantir_usuario(dados, user_id):
    if str(user_id) not in dados:
        dados[str(user_id)] = {
            "tiros": 0,
            "moedas": 0,
            "cartas": []
        }

# /inventario: mostra os dados do jogador
async def inventario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name

    dados = carregar_dados_usuarios()
    garantir_usuario(dados, user_id)

    user_data = dados[str(user_id)]

    tiros = user_data["tiros"]
    moedas = user_data["moedas"]
    quantidade_cartas = len(user_data["cartas"])

    mensagem = (
        f"📦 Inventário de {nome}:\n\n"
        f"🎯 Tiros disponíveis: {tiros}\n"
        f"💰 Moedas: {moedas}\n"
        f"🃏 Cartas únicas: {quantidade_cartas}"
    )

    await update.message.reply_text(mensagem)

# Exporta o handler
inventario_handler = CommandHandler("inventario", inventario)

