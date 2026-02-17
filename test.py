import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN','')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID','0'))

import os
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True  # Habilitar el intent de contenido de mensajes

# Crear el bot con los intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Código adicional del bot aquí...

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Ejecutar el bot
bot.run(TOKEN)
