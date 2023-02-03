import discord
from src.util.config import Config
from src.util.chatgpt import AiUtil
from src.util.database import dbUtils
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
from datetime import datetime

class PromptCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask ChatGPT a question.")
    async def prompt_command(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        try:

            context_id = await dbUtils().check_user(discord_user_id=interaction.user.id)
            if not context_id:
                embed = discord.Embed(title="ChatGPT - Error", description="User Data Issue",color=0xb34760)
                embed.add_field(name="Error", value=f"```You need to start a conversation with ChatGPT first. Go to the channel where the panel is to start.```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            else:
                user_name = interaction.user
                username = user_name.name.split("#")[0].lower()
                channel_name = interaction.channel.name
                if not channel_name == f"{username}-chatgpt":
                    embed = discord.Embed(title="ChatGPT - Error", description="Wrong Channel",color=0xb34760)
                    embed.add_field(name="Error", value=f"```You need to use this command in your ChatGPT channel.```", inline=False)
                    embed.set_footer(text="ChatGPT Discord Bot")
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    return
                response = await AiUtil().get_prompt(prompt)
                response = response.choices[0].text
        
            if "```" in response:
                parts = response.split("```")
                await interaction.followup.send(parts[0], ephemeral=True)
                code_block = "".join(line[:1900] + "\n" if len(line) > 1900 else line + "\n" for line in parts[1].split("\n"))
                code_block_chunks = [code_block[i:i+1900] for i in range(0, len(code_block), 1900)]
                for chunk in code_block_chunks:
                    embed = discord.Embed(title="ChatGPT", color=0xc29ed2)
                    embed.add_field(name="Prompt", value=f"```{prompt}```", inline=False)
                    embed.add_field(name="Response", value=f"```{chunk}```", inline=False)
                    embed.set_footer(text="ChatGPT Discord Bot")
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed, ephemeral=True)
                if len(parts) >= 3:
                    embed = discord.Embed(title="ChatGPT", color=0xc29ed2)
                    embed.add_field(name="Prompt", value=f"```{prompt}```", inline=False)
                    embed.add_field(name="Response", value=f"```{parts[2]}```", inline=False)
                    embed.set_footer(text="ChatGPT Discord Bot")
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed, ephemeral=True)
            elif len(response) > 1900:
                response_chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                for chunk in response_chunks:
                    embed = discord.Embed(title="ChatGPT", color=0xc29ed2)
                    embed.add_field(name="Prompt", value=f"```{prompt}```", inline=False)
                    embed.add_field(name="Response", value=f"```{chunk}```", inline=False)
                    embed.set_footer(text="ChatGPT Discord Bot")
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="ChatGPT", color=0xc29ed2)
                embed.add_field(name="Prompt", value=f"```{prompt}```", inline=False)
                embed.add_field(name="Response", value=f"```{response}```", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed, ephemeral=True)
        
        except Exception as e:
            embed = discord.Embed(title="ChatGPT - Error", description="The bot encountered an error:",color=0xb34760)
            embed.add_field(name="Report this to the Staff", value=f"`We couldn't get a prompt, report it to the staff, please.`", inline=False)
            embed.set_footer(text="ChatGPT Discord Bot")
            embed.set_image(url="https://i.imgur.com/98NAOch.gif")
            embed.timestamp = datetime.utcnow()
            await interaction.followup.send(embed=embed, ephemeral=True)

    @prompt_command.error
    async def prompt_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(PromptCmd(bot))