# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
from core.classes import Cog_Extension

import os
from typing import Final
from dotenv import load_dotenv
# 加載 .env 文件中的環境變量
load_dotenv()
# 特別註解 TOKEN 為字串且賦值後不應該更改
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
SERVER_ID: Final[int] = int(os.getenv('SERVER_ID'))
QUIT_CHANNEL_ID: Final[int] = int(os.getenv('QUIT_CHANNEL_ID'))
WELCOME_CHANNEL_ID: Final[int] = int(os.getenv('WELCOME_CHANNEL_ID'))


class React(Cog_Extension):
    @commands.command()
    async def localimg(self,ctx):
        dcFile = discord.File('./pics/dalle-discord-bot-logo.webp')
        await ctx.send(file=dcFile,spoiler=True)
    
    @commands.command(name="greet", help="This command greets the user.")
    async def greet_user(self,ctx):
        await ctx.send(f"Hello, {ctx.author.name}!")

    @commands.command(name="info", help="Displays information about the bot.")
    async def info(self,ctx):
        await ctx.send("測試文字")

        
    @commands.command()
    async def hello(self,ctx):
        # 列出 ctx 所有的屬性和方法
        # print(dir(ctx))
        await ctx.send(f"Message content: {ctx.message.content}")
        await ctx.send(f"Author: {ctx.author}")
        await ctx.send(f"Channel: {ctx.channel}")
        await ctx.send(f"Server: {ctx.guild}")

    @commands.command()
    async def ser_owner(self,ctx):
        guild = bot.get_guild(SERVER_ID)
        # print(dir(guild))
        owner = guild.owner_id
        await ctx.send(owner)
    
async def setup(bot):
    await bot.add_cog(React(bot))

