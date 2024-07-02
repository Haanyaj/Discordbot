import discord
from discord.ext import commands
import os

# Remplacez par votre token Discord
TOKEN = os.getenv('GITHUB_TOKEN')
print(TOKEN)
intents = discord.Intents.all()
print(intents)
bot = commands.Bot(command_prefix='!', intents=intents)
# Initialisez le client Discord
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Nous avons été connectés en tant que {client.user}')

@client.event
async def on_message(message):
    # Évitez que le bot ne réponde à ses propres messages
    if message.author == client.user:
        return

    # Cherche les URLs correspondant au modèle et les modifie
    if 'https://x.com' in message.content:
        print(message.content)
        modified_content = message.content.replace('https://x.com', 'https://vxtwitter.com')
        
        # Supprimer le message de l'utilisateur
        await message.delete()
        
        # Envoyer le message modifié
        response = f"Envoyé par: {message.author.mention}\n{modified_content}"
        await message.channel.send(response)


# Lance le bot
client.run(TOKEN)
