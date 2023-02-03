from src.util.database import dbUtils
from src.util.config import Config
from src.view.openChatView import OpenChat
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord.ui import Select, View, Button
from discord import app_commands, SelectOption
from datetime import datetime
import discord, pymysql

class Panel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Info about a product command
    @app_commands.command(name="panel", description="Send the panel to open new chats.")
    @app_commands.checks.has_permissions(administrator=True)
    async def panel_command(self, interaction: discord.Interaction):
        await interaction.response.defer()
        desc = "From here you can open a chat with the ChatGPT Bot."
        embed = discord.Embed(title="Main Menu", description=desc, color=0xc29ed2)
        embed.set_image(url="https://i.imgur.com/98NAOch.gif")
        embed.set_footer(text="ChatGPT Discord Bot")
        embed.timestamp = datetime.utcnow()
        await interaction.followup.send(embed=embed, view=OpenChat())

    @panel_command.error
    async def panel_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Panel(bot))