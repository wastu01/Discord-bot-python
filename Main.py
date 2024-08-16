""" 

學習 discord bot with python

"""

import os
from typing import Final
from dotenv import load_dotenv
# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands

# 加載 .env 文件中的環境變量
load_dotenv()
# 特別註解 TOKEN 為字串且賦值後不應該更改
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
SERVER_ID: Final[int] = int(os.getenv('SERVER_ID'))
QUIT_CHANNEL_ID: Final[int] = int(os.getenv('QUIT_CHANNEL_ID'))
WELCOME_CHANNEL_ID: Final[int] = int(os.getenv('WELCOME_CHANNEL_ID'))

print(type(WELCOME_CHANNEL_ID))
# print(TOKEN)



# bot是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = "%", intents = intents)

# 調用event函式庫
@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    print("已加入的伺服器:")
    for guild in bot.guilds:
        print(f"{guild.name} (ID: {guild.id})")
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    print(channel)
    # print(bot.guilds[0])
    if channel:
        print("here")
        owner = guild.owner.name
        owner_nick = guild.owner.nick
        await channel.send(f"owner name is {owner},{owner_nick}")


@bot.event
# 當頻道有新訊息時觸發
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == bot.user:
        return

    # 排除系統訊息，僅處理用戶發送的正常訊息
    if message.type == discord.MessageType.default:
        if message.content:
            # 打印接收到的訊息內容到控制台
            print(f"收到訊息: {message.content}")
            
            # 回覆用戶訊息，告訴他們我們已接收到
            await message.channel.send(f"你剛剛說了: {message.content}")
        

    # 如果訊息內容為 "Hello"，回覆 "Hello, world!"
    if message.content == "Hello":
        await message.channel.send("Hello, world!")

    # 如果訊息是以 '%' 開頭，表示它可能是一個指令
    # if message.content.startswith("%"):
    #     # 打印指令檢測消息到控制台
    #     print("偵測到指令:")

    # 最後再一次確保指令被正確處理，這是雙重保險
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    # 獲取發送歡迎訊息的頻道
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    
    # 發送歡迎訊息
    if channel:
        await channel.send(f"歡迎 {member.mention} 加入我們的伺服器！")

    print(f"{member} 加入了伺服器！")

@bot.event
async def on_member_remove(member):
    # 獲取發送離開訊息的頻道
    channel = bot.get_channel(QUIT_CHANNEL_ID)
    
    # 發送離開訊息
    if channel:
        await channel.send(f"{member.mention} 已離開伺服器，期待你再回來！")
    
    print(f"{member} 離開了伺服器！")

      
@bot.command()
async def hello(ctx):
    # 列出 ctx 所有的屬性和方法
    # print(dir(ctx))
    await ctx.send(f"Message content: {ctx.message.content}")
    await ctx.send(f"Author: {ctx.author}")
    await ctx.send(f"Channel: {ctx.channel}")
    await ctx.send(f"Server: {ctx.guild}")

@bot.command()
async def ser_owner(ctx):
    guild = bot.get_guild(SERVER_ID)
    # print(dir(guild))
    owner = guild.owner_id
    await ctx.send(owner)

@bot.command()
async def ping(ctx):
    await ctx.send(f"{bot.latency*1000:.6f} (ms)")
    

bot.run(TOKEN)
# bot.run(data["TOKEN"])
