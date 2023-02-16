import discord
from discord.ext import commands
import asyncio
import string
import json
import sqlite3


class Banwords(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game('Chat control'))
        global base
        global cur
        print('Bot started')
        base = sqlite3.connect('SovBot.db')
        cur = base.cursor()
        if base:
            print('DataBase connected...OK!')

    @commands.command()
    async def status(self, ctx):
        base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(
            ctx.message.guild.name))
        base.commit()
        warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(
            ctx.message.guild.name), (ctx.message.author.id,)).fetchone()
        if warning == None or warning[1] == 0:
            await ctx.send(f'{ctx.message.author.mention}, у вас немає попереджень!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, кількість попереджень: {warning[1]}!!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}\
                .intersection(set(json.load(open('cz.json')))) != set():
            await message.delete()
            name = message.guild.name
            base.execute(
                'CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
            base.commit()
            warning = cur.execute(
                'SELECT * FROM {} WHERE userid == ?'.format(name), (message.author.id, )).fetchone()
            if warning == None:
                cur.execute('INSERT INTO {} VALUES(?, ?)'.format(
                    name), (message.author.id, 1))
                base.commit()
                await message.channel.send(f'{message.author.mention}, Перше попередження, за 3 попередження - МУТ!')
            elif warning[1] == 0:
                cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(
                    name), (1, message.author.id))
                base.commit()
                await message.channel.send(f'{message.author.mention}, Перше попередження, за 3 попередження - МУТ!')
            elif warning[1] == 1:
                cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(
                    name), (2, message.author.id))
                base.commit()
                await message.channel.send(f'{message.author.mention}, Друге попередження, за 3 попередження - МУТ!')
            elif warning[1] >= 2:
                await message.channel.send(f':white_check_mark: Бан в чаті на 10 хвилин для {message.author.mention}.')
                await message.channel.set_permissions(message.author, send_messages=False)
                await asyncio.sleep(60)
                await message.channel.set_permissions(message.author, send_messages=True)
                await message.channel.send(f":white_check_mark: {message.author.mention} виходить з мута.")
                cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(
                    name), (0, message.author.id))
                base.commit()


async def setup(bot):
    await bot.add_cog(Banwords(bot))
