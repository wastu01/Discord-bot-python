""" 

學習 discord bot with python

"""


# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
# client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = "%", intents = intents)

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {client.user}")

@client.event
# 當頻道有新訊息
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return
    # 新訊息包含Hello，回覆Hello, world!
    if message.content == "Hello":
        await message.channel.send("Hello, world!")
        
@bot.command()
# 輸入%Hello呼叫指令
async def Hello(ctx):
    # 回覆Hello, world!
    await ctx.send("Hello, world!")

client.run("MTI3MDU1NjY4NjAwODE4ODk5OA.GVPkvf.1r1leGKywGYX_4mU9BTKV09ZzSIv42LgS398tI")


