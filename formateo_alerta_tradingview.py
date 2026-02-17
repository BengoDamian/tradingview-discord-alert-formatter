import os
from dotenv import load_dotenv
load_dotenv()

import json
from discord.ext import commands
import discord

# Configuraciones del bot
TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')  # set en .env o variables de entorno
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '0'))  # set en .env o variables de entorno

# Crear intents
intents = discord.Intents.default()
intents.message_content = True

# Inicializar el bot con intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} ha iniciado.')

@bot.event
async def on_message(message):
    # Evitar que el bot responda a sí mismo
    if message.author == bot.user:
        return

    # Procesar mensajes de TradingView
    if message.content.startswith('ALERTA:'):
        # Aquí puedes formatear el mensaje según tus necesidades
        data = json.loads(message.content)
        
        ticker = data.get('ticker', 'N/A')
        close = data.get('close', 'N/A')
        interval = data.get('interval', 'N/A')
        time = data.get('time', 'N/A')
        comentario = data.get('comentario', 'N/A')  # Asegúrate de que esto esté en el mensaje original
        
        formatted_message = (
            f"🔔 **ALERTA: {ticker}**\n"
            f"💲 **Precio: {close}**\n"
            f"🕒 **Temporalidad: {interval}**\n"
            f"📅 **Fecha: {time}**\n"
            f"✍️ **Comentario: {comentario}**"
        )

        # Enviar el mensaje al canal
        channel = bot.get_channel(1286939551637704745)
        if channel:
            await channel.send(formatted_message)

# Ejecutar el bot
if not TOKEN or CHANNEL_ID == 0:
    raise SystemExit('Faltan DISCORD_BOT_TOKEN o DISCORD_CHANNEL_ID (ver .env.example)')

bot.run(TOKEN)
