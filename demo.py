""" 

學習 discord bot with python

"""

import os
import json
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

# print(type(WELCOME_CHANNEL_ID))
# print(TOKEN)

with open("./setting.json",mode="r",encoding="utf8") as f:
    data = json.load(f)
    print(data["IMAGES"])


# bot是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = "!", intents = intents)

# @event 當事件發生時
@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    print("已加入的伺服器:")
    for guild in bot.guilds:
        print(f"{guild.name} (ID: {guild.id})")
    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    # print(bot.guilds[0])
    print(type(bot))
    # print(dir(bot))
    if channel:        
        owner = guild.owner.name
        owner_nick = guild.owner.nick if guild.owner.nick else owner  # 使用名稱作為暱稱的默認值
        await channel.send(f"伺服器的管理員是 {owner}, 名字叫做 {owner_nick}")


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


# @command 下指令
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cmds.{extension}")
    await ctx.send(f"loading{extension}done")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"unloading{extension}done")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cmds.{extension}")
    await ctx.send(f"reloading{extension}done")


# !delete_one_msg
@bot.command()
async def delete_one_msg(ctx, channel_id: int, message_id: int):
    await ctx.message.delete()

# !delete_specific_msg
@bot.command()
async def delete_specific_msg(ctx, message_id: int):
    # 獲取當前頻道
    channel = ctx.channel
    try:
        # 獲取並刪除指定的訊息
        message = await channel.fetch_message(message_id)
        await message.delete()
        await ctx.send("訊息已刪除")
    except discord.NotFound:
        await ctx.send("找不到訊息")
    except discord.Forbidden:
        await ctx.send("無法刪除訊息，權限不足")
    except discord.HTTPException as e:
        await ctx.send(f"刪除訊息時發生錯誤: {e}")
        
    
    
import asyncio
async def main():
    for filename in os.listdir("./cmds"):
        if filename.endswith("py"):
            await bot.load_extension(f"cmds.{filename[:-3]}")
            print(filename)
    await bot.start(TOKEN)

        
if __name__=="__main__":
    asyncio.run(main())
    
# https://fakeimg.pl/350x200/?text=Hello


# bot.run(data["TOKEN"])
