import discord
from src.util.config import Config
from src.util.chatgpt import AiUtil
from src.util.database import dbUtils
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
from datetime import datetime

class RevokeQueueCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="revoke", description="Revoke someone from the queue.")
    @app_commands.checks.has_permissions(administrator=True)
    async def revoke_command(self, interaction: discord.Interaction, user_id: discord.Member):
        await interaction.response.defer()

        try:

            userId = user_id.id
            response = await dbUtils().check_user(discord_user_id=userId)
            if response:
                await dbUtils().delete_user(discord_user_id=userId)
                embed = discord.Embed(title="ChatGPT - Finished", description="Session revoked successfully", color=0xc9b479)
                embed.add_field(name="Conversation Finished", value=f"Successfully revoked {user_id.mention}'s session.", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="ChatGPT - Error", description="User not in queue",color=0xb34760)
                embed.add_field(name="Error", value=f"Sorry, {user_id.mention} doesn't have a current session in the queue.", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            print(e)
            embed = discord.Embed(title="ChatGPT - Error", description="Error revoking user",color=0xb34760)
            embed.add_field(name="Error", value=f"Sorry, there was an error revoking {user_id.mention}.", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed, ephemeral=True)

    @revoke_command.error
    async def revoke_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RevokeQueueCmd(bot))