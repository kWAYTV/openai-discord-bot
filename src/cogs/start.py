import discord
from src.util.config import Config
from src.util.chatgpt import AiUtil
from src.util.database import dbUtils
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
from datetime import datetime

class StartConvoCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="start", description="Start a conversation with ChatGPT so he can remember your previous questions.")
    async def start_command(self, interaction: discord.Interaction):
        await interaction.response.defer()

        #if Config().bot_allowed_role in [role.id for role in interaction.user.roles]:
            
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

    @start_command.error
    async def start_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(StartConvoCmd(bot))