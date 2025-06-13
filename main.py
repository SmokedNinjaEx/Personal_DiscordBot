import discord
from discord.ext import commands
import os
import asyncio

from help_cog import help_cog # Importing help_cog from the help_cog.py file
from music_cog import music_cog # Importing music_cog from the music_cog.py file
from meme_cog import meme_cog # Importing meme_cog from the meme_cog.py file

intents = discord.Intents.default() # Default intents
intents.message_content = True # Enabling message content intent

bot = commands.Bot(command_prefix='!', intents=intents) # Creating a bot instance with the command prefix '!' and the specified intents

bot.remove_command('help') # Removing the default help command to use a custom one

async def setup(): # Function to set up the bot and add cogs
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(meme_cog(bot))
    
@bot.event # Event that triggers when the bot is ready
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    await on_ready()
    
async def main(): # Main function to run the bot
    await setup()
    await bot.start('Put discord token here') # Replace with your bot's token

asyncio.run(main()) # Running the main function to start the bot
