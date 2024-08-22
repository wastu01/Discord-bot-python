# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
from core.classes import Cog_Extension


class Main(Cog_Extension):
        
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"{self.bot.latency*1000:.6f} (ms)")
        

async def setup(bot):
    await bot.add_cog(Main(bot))