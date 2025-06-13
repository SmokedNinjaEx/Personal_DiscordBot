import discord
from discord.ext import commands
import requests
import json

class meme_cog(commands.Cog): # Meme cog to fetch random memes and dark memes
    def __init__(self, bot):
        self.bot = bot
        self.meme_api_url = "https://meme-api.com/gimme"

    @commands.command(name='meme', help="Fetches a random meme", aliases=['m']) # Command to fetch a random meme
    async def meme(self, ctx):
        response = requests.get(self.meme_api_url)
        if response.status_code == 200:
            data = response.json()
            meme_url = data['url']
            await ctx.send(meme_url)
        else:
            await ctx.send("Failed to fetch a meme. Please try again later.")
            
    @commands.command(name='dark_meme', help="Fetches a random dark meme", aliases=['dm']) # Command to fetch a random dark meme
    async def dark_meme(self, ctx):
        response = requests.get(f"{self.meme_api_url}/distressingmemes")
        if response.status_code == 200:
            data = response.json()
            meme_url = data['url']
            await ctx.send(meme_url)
        else:
            await ctx.send("Failed to fetch a dark meme. Please try again later.")