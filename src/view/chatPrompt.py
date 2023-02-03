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

            nChannel = interaction.channel.name
            nUser = "chatgpt-"+str(interaction.user.id)
            if not nChannel == nUser:
                embed = discord.Embed(title="ChatGPT - Error", description="Not your channel",color=0xb34760)
                embed.add_field(name="Error", value=f"Sorry, but this is not your channel. Please use <#{Config().panel_channel_id}> to ask questions.", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)
                return

            response = await dbUtils().check_user(discord_user_id=interaction.user.id)
            if response:
                embed = discord.Embed(title="ChatGPT - Error", description="Conversation already started",color=0xb34760)
                embed.add_field(name="Error", value=f"```Sorry, but you already have a conversation with ChatGPT. Please use /ask in your chatgpt channel to ask a question.```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)
                return
            else:
                total_users = await dbUtils().get_total_users()
                if total_users >= Config().max_chats:
                    delchannel = interaction.channel
                    embed = discord.Embed(title="ChatGPT - Error", description="Queue is full",color=0xb34760)
                    embed.add_field(name="Error", value=f"```Sorry, but the queue is full of people talking to ChatGPT. Please try again later.```", inline=False)
                    embed.add_field(name="Deleting Channel", value="`Your channel will be deleted in 5 seconds.`", inline=False)
                    embed.set_footer(text="ChatGPT Discord Bot")
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed)
                    time.sleep(5)
                    await delchannel.delete()
                    return
                
                await dbUtils().add_user(discord_user_id=interaction.user.id, channel_id= interaction.channel.id, context_id="test")
                embed = discord.Embed(title="ChatGPT - Success", color=0x00ff00)
                embed.add_field(name="Conversation started", value=f"```You can now ask with ChatGPT for the next 15 minutes. Use /ask to ask him a question.```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)

        except Exception as e:
            print(e)
            embed = discord.Embed(title="ChatGPT - Error", description="An error occured",color=0xb34760)
            embed.add_field(name="Error", value=f"```Sorry, but we couldn't start your convo, try again later.```", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(label='Delete channel!', style=discord.ButtonStyle.red, custom_id='delete-channel-button', emoji = '🗑️')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        try:
            
            response = await dbUtils().check_user(discord_user_id=interaction.user.id)
            if response:
                await dbUtils().delete_user(discord_user_id=interaction.user.id)
                channel = interaction.channel
                embed = discord.Embed(title="ChatGPT - Finished", description="Conversation finished successfully", color=0xc9b479)
                embed.add_field(name="Conversation Finished", value=f"You can use <#{Config().panel_channel_id}> to start a conversation anytime again.", inline=False)
                embed.add_field(name="Deleting Channel", value="`Your channel will be deleted in 5 seconds.`", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)
                time.sleep(5)
                await channel.delete()
                return
            else:
                embed = discord.Embed(title="ChatGPT - Error", description="Conversation not started",color=0xb34760)
                embed.add_field(name="Error", value=f"Sorry, but you don't have a conversation with ChatGPT. Please use <#{Config().panel_channel_id}> to start a conversation.", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)
                nChannel = interaction.channel.name
                nUser = "chatgpt-"+str(interaction.user.id)
                if not nChannel == nUser:
                    await interaction.channel.delete()
                return
        
        except Exception as e:
            print(e)
            embed = discord.Embed(title="ChatGPT - Error", description="Error finishing conversation",color=0xb34760)
            embed.add_field(name="Error", value=f"```Sorry, but there was an error finishing your conversation.```", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

    @discord.ui.button(label='Help!', style=discord.ButtonStyle.blurple, custom_id='help-button', emoji = '❓')
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        try:

            embed = discord.Embed(title="ChatGPT - Help", color=0x00ff00)
            embed.add_field(name="Help", value=f"```Press the `Start Asking!` button and then use /ask to ask ChatGPT a question.\nUse `/` and click the Bot icon to check a list of available commands```", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(e)
            embed = discord.Embed(title="ChatGPT - Error", description="An error occured",color=0xb34760)
            embed.add_field(name="Error", value=f"```Sorry, but we couldn't send you the help message, try again later.```", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed)