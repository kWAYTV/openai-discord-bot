import discord
from src.util.config import Config
from src.util.chatgpt import AiUtil
from src.util.database import dbUtils
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
from datetime import datetime

class CurrentUsersCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="current", description="See who's taking the spots right now.")
    async def current_command(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            response = await dbUtils().get_discord_ids()

            if response:
                users = ""
                embed = discord.Embed(title="ChatGPT - Queue", color=0xc9b479)
                for user in response:
                    users += f"<@{user[0]}>\n"
                embed.add_field(name="Current users in queue", value=f"{users}", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
            else:
                embed = discord.Embed(title="ChatGPT - Current Users", description="Current users in queue", color=0xc9b479)
                embed.add_field(name="User", value=f"```No users in queue```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
            
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(e)
            embed = discord.Embed(title="ChatGPT - Error", description="Error getting current users",color=0xb34760)
            embed.add_field(name="Error", value=f"```Sorry, but there was an error getting current users.```", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

    @current_command.error
    async def current_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CurrentUsersCmd(bot))