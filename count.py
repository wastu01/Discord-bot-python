# 1277565731579363338
# 713777558994550888
import re
import os
import discord
from discord.ext import commands, tasks
import asyncio
from typing import Final
from dotenv import load_dotenv
load_dotenv()
TOKEN: Final[str] = os.getenv('SELF_TOKEN')

print(TOKEN)

# 自訂 Bot 的命令前綴與參數
# 設定 Self-Bot，這裡不需要 intents
bot = commands.Bot(command_prefix="!", self_bot=True, chunk_guilds_at_startup=False)

channel_id = 1270556602801455175  # 替換為您的實際頻道 ID
allowed_ids = [713777558994550888]  # 許可的用戶 ID 列表

# 移除預設的幫助命令
bot.remove_command('help')

# 編譯正則表達式，這次捕捉整個運算式
expression_pattern = re.compile(r'[\d\+\-\*\/\(\)]+')

def generate_sequence(n):
    # 生成遞增和遞減數列
    sequence = list(range(1, n + 2)) + list(range(n, 0, -1))
    return sequence

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    global count
    count = 0  # 初始化 count
    channel = bot.get_channel(channel_id)
    
    # 讀取頻道歷史訊息的最新一筆
    async for message in channel.history(limit=1):
        try:
            # 檢查是否為有效的運算式（只允許數字）
            if message.content.isdigit():
                count = int(message.content)  # 將訊息轉換為整數
                sequence = generate_sequence(count)  # 生成遞增遞減數列
                result = sum(sequence) / (count + 1)  # 計算結果
                print(f"生成的數列: {sequence}")
                print(f"計算結果: {result}")
            else:
                print(f"無效的運算式: {message.content}")
        except Exception as e:
            print(f'運算錯誤: {e}')
            count = 1  # 如果出錯，重新開始計數

    count_numbers.start()

@tasks.loop(seconds=5.9)
async def count_numbers():
    global count  # 確保使用的是全域變數 count
    try:
        channel = bot.get_channel(channel_id)
        # 檢查 bot 是否有權限在頻道中發送訊息
        if channel and channel.permissions_for(channel.guild.me).send_messages:
            # 根據前一位的輸入生成運算式
            sequence = generate_sequence(count)  # 生成遞增遞減數列
            expression = f"({'+'.join(map(str, sequence))})/{count + 1}"
            await channel.send(expression)  # 發送生成的運算式
            print(f"Sent: {expression}")
            count += 1  # 更新 count
        await asyncio.sleep(2)
    except Exception as e:
        print(f'Error: {e}')

@bot.event
async def on_message(message):
    global count  # 確保使用的是全域變數 count

    # 終止命令 "!q" 用於結束並重啟
    if message.content == "!q":
        await message.channel.send("機器人即將重啟...")
        await bot.close()  # 結束 bot
        print("機器人已關閉")
        return

    # 檢查是否為指定的頻道
    if message.channel.id != channel_id:
        return

    # 檢查是否為 bot 發送的訊息
    if message.author.bot:
        print(f'Bot 發送的訊息: {message.content}')
        await message.channel.send(f"<@{message.author.id}> 在 **{count}** 之後數錯了！！下一個數字是 **1**。**數錯了。**")
        count = 1  # 從1重新開始
        return

    # 處理有效的運算式
    try:
        if message.content.isdigit():
            count = int(message.content)  # 讀取前一位輸入的數字
            sequence = generate_sequence(count)  # 生成遞增遞減數列
            result = sum(sequence) / (count + 1)  # 計算運算結果
            print(f'新計算結果: {result}')
        else:
            print(f"無效的運算式: {message.content}")
    except Exception as e:
        print(f'運算錯誤: {e}')
        count = 1  # 若運算錯誤，重新開始
    await bot.process_commands(message)

bot.run(TOKEN)
