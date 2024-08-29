import os
from typing import Final
from dotenv import load_dotenv
# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
from core.classes import Cog_Extension

# 加載 .env 文件中的環境變量
load_dotenv()
# 特別註解 TOKEN 為字串且賦值後不應該更改
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
SERVER_ID: Final[int] = int(os.getenv('SERVER_ID'))
QUIT_CHANNEL_ID: Final[int] = int(os.getenv('QUIT_CHANNEL_ID'))
WELCOME_CHANNEL_ID: Final[int] = int(os.getenv('WELCOME_CHANNEL_ID'))

class Event(Cog_Extension):
        
    @commands.Cog.listener()
    async def on_member_join(self,member):
        # 獲取發送歡迎訊息的頻道
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        server_name = member.guild.name
        # 發送歡迎訊息
        if channel:
            await channel.send(f"歡迎 {member.mention} 加入我們的伺服器 {server_name}！")

        print(f"{member} 加入了伺服器！")

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        # 獲取發送離開訊息的頻道
        channel = self.bot.get_channel(QUIT_CHANNEL_ID)
        
        # 發送離開訊息
        if channel:
            await channel.send(f"{member.mention} 已離開我們的伺服器，期待你再回來！")
        
        print(f"{member} 離開了伺服器！")
    
    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content.endswith("你好"):
            await msg.channel.send("123")

        

async def setup(bot):
    await bot.add_cog(Event(bot))