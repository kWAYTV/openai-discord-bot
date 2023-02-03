from ..util.config import Config
from colorama import Fore, init, Style
from src.util.database import dbUtils
from src.util.chatgpt import AiUtil
import discord, os, time, requests, json, dotenv, logging, asyncio, httpx, pymysql
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord.ui import Select, View, Button
from discord import app_commands, SelectOption
from itertools import cycle
from colorama import Fore, init, Style
from dotenv import load_dotenv
from threading import Timer
from datetime import datetime
from math import log10 , floor

class ChatPrompt(View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Start asking!', style=discord.ButtonStyle.green, custom_id='start-asking-button', emoji = '🎫')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        try:

            response = await dbUtils().check_user(discord_user_id=interaction.user.id)
            if response:
                embed = discord.Embed(title="ChatGPT - Error", description="Conversation already started",color=0xb34760)
                embed.add_field(name="Error", value=f"```Sorry, but you already have a conversation with ChatGPT. Please use /ask to ask him a question.```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            else:
                total_users = await dbUtils().get_total_users()
                if total_users >= Config().max_chats:
                    embed = discord.Embed(title="ChatGPT - Error", description="Queue is full",color=0xb34760)
                    embed.add_field(name="Error", value=f"```Sorry, but the queue is full of people talking to ChatGPT. Please try again later.```", inline=False)
                    embed.set_footer(text="ChatGPT Discord Bot")
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return

                prompt = await AiUtil().get_prompt("Hello, i'm talking to you from my Discord bot, i will ask you some questions now.")
                await dbUtils().add_user(discord_user_id=interaction.user.id, context_id=prompt.id)
                embed = discord.Embed(title="ChatGPT - Success", color=0x00ff00)
                embed.add_field(name="Conversation started", value=f"```You can now ask with ChatGPT for the next 15 minutes. Use /ask to ask him a question.```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(e)
            embed = discord.Embed(title="ChatGPT - Error", description="An error occured",color=0xb34760)
            embed.add_field(name="Error", value=f"```Sorry, but we couldn't start your convo, try again later.```", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed, ephemeral=True)