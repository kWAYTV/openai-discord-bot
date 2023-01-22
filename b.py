# Imports
import discord, os, time, requests, json, logging, asyncio, httpx, pymysql
from src.util.config import Config
from src.util.database import dbUtils
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
from itertools import cycle
from colorama import Fore, init, Style
from threading import Timer
from datetime import datetime
from math import log10 , floor

# Clear function
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear") # Don't touch this.
clear()

class Bot(commands.Bot):

    async def setup_hook(self) -> None:
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Starting the bot...")
        for filename in os.listdir("./src/cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}] {Fore.RESET}Loaded cog {filename[:-3]}")
                await self.load_extension(f"src.cogs.{filename[:-3]}")

# Define the clients
connection = pymysql.connect(host=Config().db_host, user=Config().db_user, password=Config().db_pass, db=Config().db_name)
bot = Bot(command_prefix=Config().bot_prefix, help_command=None, intents=discord.Intents.all())

# Dynamic activity
status = cycle(["discord.gg/kws", "kwayservices.top", "discord.gg/fml"])
@tasks.loop(seconds=30)
async def changeStatus():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

# Delete expired users
@tasks.loop(seconds=60)
async def deleteExpiredUsers():
    await dbUtils().deleteExpiredUsers()

# On Ready Event
@bot.event
async def on_ready():
    clear()
    print(f"{Fore.MAGENTA}> {Fore.RESET}Logged in as {bot.user.name}#{bot.user.discriminator}.")

    await dbUtils().create_table()

    logging.basicConfig(handlers=[logging.FileHandler('openai-dc.log', 'a+', 'utf-8')], level=logging.INFO, format='%(asctime)s: %(message)s')

    changeStatus.start()
    deleteExpiredUsers.start()

# Sync slash commands
@bot.command()
async def sync(ctx):
    try:
        await ctx.message.delete()
        await bot.tree.sync()
        msg = await ctx.send("Done!")
        time.sleep(2)
        await msg.delete()
        print(f"{Fore.GREEN}[{Fore.RESET}+{Fore.GREEN}] {Fore.RESET}Synced slash commands!")
    except Exception as e:
        print(f"{Fore.RED}[{Fore.RESET}-{Fore.RED}] {Fore.RESET}Error: {e}")

if __name__ == "__main__":
    try:
        bot.run(Config().bot_token)
    except KeyboardInterrupt:
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Closing the bot...")
        connection.close()
        print(f"{Fore.MAGENTA}>{Fore.WHITE} Closed connection.")
        exit()