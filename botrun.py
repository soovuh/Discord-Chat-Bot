import discord
from discord.ext import commands
import os


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        initial_extensions = []
        for filename in os.listdir('.\\cogs'):
            if filename.endswith('.py'):
                initial_extensions.append('cogs.' + filename[:-3])
        self.initial_extensions = initial_extensions

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)         

TOKEN = 'Your bot TOKEN'

bot = MyBot()
bot.run(os.getenv(TOKEN))
