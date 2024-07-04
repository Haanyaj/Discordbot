import os
import discord
from discord.ext import commands

# Charger les variables d'environnement
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN is None:
    raise ValueError("No DISCORD_BOT_TOKEN found in environment variables")

print(f"Token loaded: {TOKEN[:5]}...")  # Affiche une partie du token pour vérifier qu'il est chargé

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Nous avons été connectés en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'https://x.com' in message.content:
        modified_content = message.content.replace('https://x.com', 'https://vxtwitter.com')
        await message.delete()
        response = f"OUAIS WALID\nDe: {message.author.mention}\n{modified_content}"
        await message.channel.send(response)

client.run(TOKEN)
