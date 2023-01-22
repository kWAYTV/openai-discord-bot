import discord
from src.util.config import Config
from src.util.chatgpt import AiUtil
from src.util.database import dbUtils
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
from datetime import datetime

class EndConvoCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="end", description="End a conversation with ChatGPT so you can leave space on the queue.")
    async def end_command(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if Config().bot_allowed_role in [role.id for role in interaction.user.roles]:
            
            response = await dbUtils().check_user(discord_user_id=interaction.user.id)
            if response:
                await dbUtils().delete_user(discord_user_id=interaction.user.id)
                embed = discord.Embed(title="ChatGPT - Success", description="Conversation finished successfully", color=0x00ff00)
                embed.add_field(name="Conversation Ended", value=f"```You can use /start to start a conversation anytime again.```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            else:
                embed = discord.Embed(title="ChatGPT - Error", description="Conversation not started",color=0xb34760)
                embed.add_field(name="Error", value=f"```Sorry, but you don't have a conversation with ChatGPT. Please use /start to start a conversation.```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

    @end_command.error
    async def end_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(EndConvoCmd(bot))