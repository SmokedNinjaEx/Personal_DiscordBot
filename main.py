import discord
from discord.ext import commands
import os
import asyncio

from help_cog import help_cog
from music_cog import music_cog
from meme_cog import meme_cog

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

async def setup():
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(meme_cog(bot))
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    await on_ready()
    
async def main():
    await setup()
    await bot.start('Put your discord token here')

asyncio.run(main())
