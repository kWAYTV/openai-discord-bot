from ..util.config import Config
from colorama import Fore, init, Style
from src.util.database import dbUtils
from src.util.chatgpt import AiUtil
from src.view.chatPrompt import ChatPrompt
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

class OpenChat(View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Try me!', style=discord.ButtonStyle.green, custom_id='open_chat_button', emoji = '💬')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):

        # Create a new text channel
        guild = interaction.guild
        user = interaction.user
        channel_name = f"{user.name}-chatgpt"

        # if there is already a channel with that name, put a number at the end
        if discord.utils.get(guild.channels, name=channel_name):
            i = 1
            while discord.utils.get(guild.channels, name=f"{channel_name}-{i}"):
                i += 1
            channel_name = f"{channel_name}-{i}"

        category = guild.get_channel(Config().chat_category_id)
        channel = await category.create_text_channel(channel_name)

        memberRole = discord.utils.get(guild.roles, id=Config().member_role_id)

        # Set permissions on the channel so that only the user can access it
        await channel.set_permissions(user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False, send_messages=False)
        await channel.set_permissions(memberRole, read_messages=False, send_messages=False)

        # Switch to the new channel
        await interaction.response.send_message(f"Switching to {channel.mention}", ephemeral=True)
        await channel.send(f"Hey! {user.mention} Welcome to your ChatGPT channel!", view=ChatPrompt())