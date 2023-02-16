import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

class Command(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, arg=None):
        author = ctx.message.author
        if arg == None:
            await ctx.send(f'{author.mention} Привіт!, я чат бот.\n!info all - загальна інформація.\n!info commands - список команд.\n')
        elif arg == 'all':
            await ctx.send(f'''{author.mention}!
Моє основне завдання - контроль та відстежування активності у чаті.
Я даю мут у чаті за образливі слова, реагую на приємні слова.
Загалом це весь мій функціонал. Щоб дізнатись більше - !info commands''')
        elif arg == 'commands':
            await ctx.send(f'''{author.mention}
!status - мій статус та попередження.
!kick - кік користувача (при наявності доступу).
''')
        else:
            await ctx.send(f'{author.mention} такої команди немає.')

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='Я можу)'):
        await member.kick(reason=reason)
        await ctx.send(f'Користувач {member.mention} був видалений.')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Ви не маєте відповідного доступу')

    # @commands.command()
    # async def chupik(self, ctx):
    #     file = discord.File('.\\media\\dj.gif', filename="dj.gif")

    #     embed = discord.Embed(title='Дуже смачно',
    #                           url='https://i.pinimg.com/564x/2e/bf/f0/2ebff099714c79cc8f36fc5a7740c316.jpg',
    #                           description='Честно кажучи', color=0xfc03d7)
    #     embed.set_author(name=ctx.author.display_name,
    #                      icon_url=ctx.author.avatar)
    #     embed.set_thumbnail(url="attachment://dj.gif")
    #     embed.add_field(name='Перший', value='стовпець', inline=True)
    #     embed.add_field(name='Другий', value='стовпець', inline=True)
    #     embed.set_footer(text='Це тестова рамка')
    #     await ctx.send(file=file, embed=embed)


async def setup(bot):
    await bot.add_cog(Command(bot))
