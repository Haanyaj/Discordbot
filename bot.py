import os
import re
import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup



# Charger les variables d'environnement
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN is None:
    raise ValueError("No DISCORD_BOT_TOKEN found in environment variables")

print(f"Token loaded: {TOKEN[:5]}...")  # Affiche une partie du token pour vérifier qu'il est chargé

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)

async def has_multi_media(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Vérifier les images multiples
            image_container = soup.find('div', {'data-testid': 'tweetPhoto'})
            if image_container and len(image_container.find_all('img')) > 1:
                return True
            
            # Vérifier la présence de vidéo
            video_container = soup.find('div', {'data-testid': 'tweetVideo'})
            if video_container:
                return True
            
    return False

@client.event
async def on_ready():
    print(f'Nous avons été connectés en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'https://x.com' in message.content:
        x_links = re.findall(r'https?://(?:www\.)?x\.com/\S+', message.content)
    
        if x_links:
            modified_content = message.content
            for link in x_links:
                if await has_multi_media(link):
                    modified_link = link.replace('https://x.com', 'https://vxtwitter.com')
                    modified_content = modified_content.replace(link, modified_link)
            
            if modified_content != message.content:
                await message.delete()
                response = f"De: {message.author.mention}\n{modified_content}"
                await message.channel.send(response)
        
    if 'https://vm.tiktok.com' in message.content:
        modified_content = message.content.replace('https://vm.tiktok.com', 'https://vm.vxtiktok.com')
        await message.delete()
        response = f"De: {message.author.mention}\n{modified_content}"
        await message.channel.send(response)
        
    if 'https://www.tiktok.com' in message.content:
        modified_content = message.content.replace('https://www.tiktok.com', 'https://vm.vxtiktok.com')
        await message.delete()
        response = f"De: {message.author.mention}\n{modified_content}"
        await message.channel.send(response)
        
    if 'https://www.instagram.com' in message.content:
        modified_content = message.content.replace('https://www.instagram.com', 'https://www.ddinstagram.com')
        await message.delete()
        response = f"De: {message.author.mention}\n{modified_content}"
        await message.channel.send(response)

client.run(TOKEN)
