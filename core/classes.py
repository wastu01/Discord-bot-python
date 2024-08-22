# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands

class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot = bot