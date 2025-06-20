import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog): # Music cog to handle music playback in voice channels
    def __init__(self, bot):
        self.bot = bot
        
        self.is_playing = False
        self.is_paused = False
        
        self.music_queue = []
        self.YDL_OPTIONS = { # YouTube DL options for extracting audio from YouTube videos
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
        }
        self.FFMPEG_OPTIONS = { # FFMPEG options for playing audio
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        
        self.vc = None
        
    def search_yt(self, item): # Function to search for a YouTube video and return its audio source and title
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(item, download=False)['entries'][0]
            except Exception:
                return False
        return {
            'source': info['formats'][0]['url'],
            'title': info['title']}
    
    def play_next(self):   # Function to play the next song in the queue
        if len(self.music_queue) > 0:
            self.is_playing = True
            self.is_paused = False
            
            m_url = self.music_queue[0]['source']
            self.music_queue.pop(0)
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            
    async def play_music(self, ctx): # Function to play music in the voice channel
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            
            if self.vc == None or not self.vc.is_connected():
                self.vc = self.music_queue[0][1].connect()
                
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel.")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
                
            self.music_queue.pop(0)
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            
    @commands.command(name='play', help="Plays the selected song from youtube", aliases=['p', 'Playing']) # Command to play a song from YouTube
    async def play(self, ctx, *args):
        query = ' '.join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Please join a voice channel.")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not find the song. Try another search term.")
            else:
                await ctx.send(f"Added to queue: {song['title']}")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)
                    
    @commands.command(name='pause', help="Pauses the current song") # Command to pause the current song
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()
        else:
            await ctx.send("No song is currently playing.")
            
    @commands.command(name='resume', help="Resumes the paused song", aliases=['r']) # Command to resume the paused song
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
        else:
            await ctx.send("No song is currently paused.")
            
    @commands.command(name='skip', help="Skips the current song", aliases=['s']) # Command to skip the current song
    async def skip(self, ctx, *args):
        if self.is_playing:
            self.vc.stop()
            await self.play_music(ctx)
        else:
            await ctx.send("No song is currently playing.")
            
    @commands.command(name='queue', help="Shows the current music queue", aliases=['q']) # Command to show the current music queue
    async def queue(self, ctx):
        retval = ""
        
        for i in range(len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + "\n"
            
        if retval == "":
            await ctx.send(retval)
        else:
            await ctx.send("There are no songs in the queue.")
            
    @commands.command(name='clear', help="Clears the current music queue", aliases=['c'])  # Command to clear the current music queue
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue has been cleared.")
    
    @commands.command(name='leave', help="Disconnects the bot from the voice channel", aliases=['l']) # Command to disconnect the bot from the voice channel
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await ctx.vc.disconnect()