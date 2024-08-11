""" 

學習 discord bot with python

"""

from typing import Final
import os
from dotenv import load_dotenv
# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands

load_dotenv()
TOKEN: Final[str] = os. getenv('DISCORD_TOKEN')

print(TOKEN)

# client是跟discord連接，intents是要求機器人的權限
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
    print(f"已加入的伺服器列表: {bot.guilds}")

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
        
        # 確保指令被正確處理，這樣命令和一般訊息可以共存
        await bot.process_commands(message)

    # 如果訊息內容為 "Hello"，回覆 "Hello, world!"
    if message.content == "Hello":
        await message.channel.send("Hello, world!")

    # 如果訊息是以 '%' 開頭，表示它可能是一個指令
    if message.content.startswith("%"):
        # 打印指令檢測消息到控制台
        print("偵測到指令")

    # 最後再一次確保指令被正確處理，這是雙重保險
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    # 獲取發送歡迎訊息的頻道
    channel = bot.get_channel(1272050945445990431)
    
    # 發送歡迎訊息
    if channel:
        await channel.send(f"歡迎 {member.mention} 加入我們的伺服器！")

    print(f"{member} 加入了伺服器！")

@bot.event
async def on_member_remove(member):
    # 獲取發送離開訊息的頻道
    channel = bot.get_channel(1272056555805605962)
    
    # 發送離開訊息
    if channel:
        await channel.send(f"{member.mention} 已離開伺服器，期待你再回來！")
    
    print(f"{member} 離開了伺服器！")

      
@bot.command()
async def hello(ctx):
    # 列出 ctx 所有的屬性和方法
    # print(dir(ctx))
    print(f"Author: {ctx.author}")
    print(f"Channel: {ctx.channel}")
    print(f"Guild: {ctx.guild}")
    print(f"Message content: {ctx.message.content}")
    await ctx.send("Hello, world!")
    
@bot.command()
async def ping(ctx):
    await ctx.send(bot.latency)
    # print("OK")
    


bot.run(TOKEN)
