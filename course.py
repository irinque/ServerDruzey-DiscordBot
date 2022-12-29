import time 
import sqlite3
import discord
import random
from discord.ext import commands
from discord.utils import get

intents = discord.Intents().all()
client = discord.Client
Token = "MTAyNzkyNjA1NjA1NDgzNzMyOQ.Geh_vr.dFSQ9bAPmfZ1Hz6yUB3XurSgmRfX-liQvvUuJA"  # Токен Бота
channel = 1042173661899149432
bot = commands.Bot(command_prefix="!", intents=discord.Intents().all())  # Параметр Бот
DATABASE = "serverdruzey3.db"

@bot.command()
async def go(ctx):
    print("go")
    channel = bot.get_channel(1042173661899149432)
    emoji1 = discord.utils.get(bot.emojis, name='shulk')
    emoji2 = discord.utils.get(bot.emojis, name='diamond')
    connect = sqlite3.connect(DATABASE)
    cursor = connect.cursor()
    while True:
        print(2)
        time.sleep(5)
        Currency = cursor.execute("SELECT standart FROM currency").fetchone()
        if random.randint(1, 2) == 1:
            cursor.execute(f"UPDATE currency SET standart = standart + {random.randint(0, 10)}")
            cursor.close()
            connect.commit()
            connect.close()
            embed = discord.Embed(
            title=f"**Валюта поднялась в цене!**",
            description=f"**1 SH {emoji1} = {Currency[0]} АР {emoji2}**",
            colour=discord.Colour.from_rgb(0, 162, 255)
            )
            await channel.send(embed=embed)
                    
        else:
            cursor.execute(f"UPDATE currency SET standart = standart - {random.randint(0, 10)}")
            cursor.close()
            connect.commit()
            connect.close()
            embed = discord.Embed(
            title=f"**Валюта упала в цене!**",
            description=f"**1 SH {emoji1} = {Currency[0]} АР {emoji2}**",
            colour=discord.Colour.from_rgb(0, 162, 255)
            )
            await channel.send(embed=embed)

    
if __name__ == "__main__":
    bot.run(Token)
    cource()
