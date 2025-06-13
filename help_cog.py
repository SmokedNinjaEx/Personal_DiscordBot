import discord
from discord.ext import commands

class help_cog(commands.Cog): # Help cog to provide information about bot commands
    def __init__(self, bot):
        self.bot = bot
        
        self.help_message = """
        '''
        General Commands:
        !help - Show this help message
        !p <song_name> - Play a song
        !q - Show the current music queue
        !s - Skip the current song
        !c - Clear the music queue
        !l - Disconnect the bot from the voice channel
        !pause - Pause the current song
        !r - Resume the paused song
        !h - Alias for !help
        !m - Fetch a random meme
        !dm - Fetch a random dark meme
        '''
        """
        
        self.text_channel = []
        
    @commands.Cog.listener() # Listener that triggers when the bot is ready
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel.append(channel)
                
        await self.send_to_all(self.help_message)
        
    async def send_to_all(self, message): # Function to send a message to all text channels
        for text_channel in self.text_channel_text:
            await text_channel.send(message)
            
    @commands.command(name='help', help="Shows all bot commands", aliases=['h']) # Command to show all bot commands
    async def help(self,ctx):
        await ctx.send(self.help_message)