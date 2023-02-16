import discord
from discord.ext import commands


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('Привіт, я чат-бот. Я відповідальний за чат!\n!info - для більш детальної інформації.')

        for ch in self.bot.get_guild(member.guild.id).channels:
            if ch.name == 'general':
                await self.bot.get_channel(ch.id).send(f'{member.mention} тепер з нами!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for ch in self.bot.get_guild(member.guild.id).channels:
            if ch.name == 'general':
                await self.bot.get_channel(ch.id).send(f'{member.mention} покинув нас, яка прикрість.')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.name == self.bot.user.name:
            return
        chnnel = reaction.message.channel
        await chnnel.send(user.mention + ' додав ' + reaction.emoji)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.name == self.bot.user.name:
            return
        chnnel = reaction.message.channel
        await chnnel.send(user.mention + ' видалив ' + reaction.emoji)

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author == self.bot.user:
            return
        words = ['гарно', 'добре', 'щастя', 'любов', 'щасливий', 'щаслива', 'кохання', 'кохаю', 'python']
        for word in words:
            if  word in message.content.lower():
                emoji = '\U0001F60D'
                await message.add_reaction(emoji)


async def setup(bot):
    await bot.add_cog(Event(bot))
