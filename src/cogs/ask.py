import discord
from src.util.config import Config
from src.util.chatgpt import AiUtil
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
from datetime import datetime

class PromptCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask ChatGPT a question")
    async def prompt_command(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        if Config().bot_allowed_role in [role.id for role in interaction.user.roles]:
            try:
                response = f"> **{prompt}** - <@{interaction.user.id}>\n{await AiUtil().get_prompt(prompt)}"
                if "```" in response:
                    parts = response.split("```")
                    await interaction.followup.send(parts[0], ephemeral=True)
                    code_block = "".join(line[:1900] + "\n" if len(line) > 1900 else line + "\n" for line in parts[1].split("\n"))
                    code_block_chunks = [code_block[i:i+1900] for i in range(0, len(code_block), 1900)]
                    for chunk in code_block_chunks:
                        await interaction.followup.send(f"```{chunk}```", ephemeral=True)
                    if len(parts) >= 3:
                        await interaction.followup.send(parts[2], ephemeral=True)
                elif len(response) > 1900:
                    response_chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                    for chunk in response_chunks:
                        await interaction.followup.send(chunk, ephemeral=True)
                else:
                    await interaction.followup.send(response, ephemeral=True)

            except Exception as e:
                await interaction.followup.send("> **Error: Something went wrong, please try again later!**")
        else:
            await interaction.followup.send("> **Error: You do not have permission to use this command!**")

    @prompt_command.error
    async def prompt_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(PromptCmd(bot))