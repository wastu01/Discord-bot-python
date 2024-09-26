import os
from dotenv import load_dotenv
# 導入 Discord.py 模組
import discord
# 導入 commands 指令模組
from discord.ext import commands

# 加載 .env 文件中的環境變量
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 設置 intents
intents = discord.Intents.default()
intents.message_content = True

# 創建 Bot 物件
bot = commands.Bot(command_prefix="!", description="A simple demo bot", strip_after_prefix=True, intents=intents)


# @event 當事件發生時
@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f'Logged in as {bot.user}')

# @listen 當訊息事件發生時
@bot.listen()
async def on_message(message):
    if message.author != bot.user:
        print('one')
        await message.channel.send(message.content)

# @command 當使用者輸入指定命令時
@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

@bot.command()
async def q(ctx):
    await bot.close()
    
@bot.command()
async def new(ctx, msg):
    guild = ctx.guild # 獲取伺服器
    await guild.create_text_channel('msg')  # 創建文本頻道


# 使用自定義事件名稱進行監聽
@bot.listen('on_message')
async def my_message(message):
    print('two')

# 啟動機器人
bot.run(TOKEN)
