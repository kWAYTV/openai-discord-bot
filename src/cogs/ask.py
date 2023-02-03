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
    async def prompt_command(self, interaction: discord.Interaction, prompt: str, reset: bool = False):
        await interaction.response.defer()

        try:

            nChannel = interaction.channel.name
            nUser = "chatgpt-"+str(interaction.user.id)
            if not nChannel == nUser:
                embed = discord.Embed(title="ChatGPT - Error", description="Conversation not started",color=0xb34760)
                embed.add_field(name="Error", value=f"Sorry, but you don't have a conversation with ChatGPT. Please use <#{Config().panel_channel_id}> to start a conversation.\nIf you have a conversation already, go to your channel and type /finish & delete the channel in the top button.", inline=False)
                embed.set_footer(text="ChatGPT Discord Bot")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)
                return

            response = await AiUtil().get_response(prompt=prompt, new_conv=reset)
            answer = response['choices'][0]['text']
            if len(answer) > 1900:
                self.page = 1
                chunks = await MsgUtil().split_string_into_chunks(answer, 1900)
                for chunk in chunks:
                    embed = discord.Embed(title=f"ChatGPT Bot - Page {self.page}", color=0x00ff00)
                    if self.page == 1:
                        embed.add_field(name="Prompt", value=f"`{prompt}`", inline=False)
                        if not "```" in answer:
                            embed.add_field(name="Response", value=f"```{chunk}```", inline=False)
                        else:
                            embed.add_field(name="Response", value=f"{chunk}", inline=False)
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Used Tokens : {response['usage']['total_tokens']}")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed)
                    self.page += 1
            else:
                embed = discord.Embed(title=f"ChatGPT Bot", color=0x00ff00)
                embed.add_field(name="Prompt", value=f"`{prompt}`", inline=False)
                if not "```" in answer:
                    embed.add_field(name="Response", value=f"```{answer}```", inline=False)
                else:
                    embed.add_field(name="Response", value=f"{answer}", inline=False)
                embed.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Used Tokens: {response['usage']['total_tokens']}")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)
            
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