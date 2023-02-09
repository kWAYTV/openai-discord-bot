import discord, httpx, urllib.parse
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
    @app_commands.describe(prompt="The question you want to ask ChatGPT.", reset="Reset the conversation with ChatGPT. (useless atm)")
    async def prompt_command(self, interaction: discord.Interaction, prompt: str, reset: bool = False):
        await interaction.response.defer()

        code = ""
        answer = ""

        try:

            nChannel = interaction.channel.name
            nUser = "chatgpt-"+str(interaction.user.id)
            if not nChannel == nUser:
                embed = discord.Embed(title="ChatGPT - Error", description="Conversation not started",color=0xb34760)
                embed.add_field(name="Error", value=f"Sorry, but you are not in your ChatGPT channel. Please use your channel or go to <#{Config().panel_channel_id}> to start a conversation.\nIf you have a conversation already, go to your channel and type /finish & delete the channel in the top button.", inline=False)
                embed.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Used Tokens : {response['usage']['total_tokens']}")
                embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                embed.timestamp = datetime.utcnow()
                await interaction.followup.send(embed=embed)
                return

            response = await AiUtil().get_response(prompt=prompt, new_conv=reset)
            raw_answer = response['choices'][0]['text']

            code, answer = await AiUtil().get_code_blocks(raw_answer)

            if len(answer) > 1900:
                answer_chunks = await AiUtil().split_string_into_chunks(answer, 1900)
                for chunk in answer_chunks:
                    embed = discord.Embed(title="ChatGPT - Answer", color=0x00ff00)
                    embed.add_field(name="Prompt", value=f"```{prompt}```", inline=False)
                    if chunk:
                        embed.add_field(name="Response", value=f"```{chunk}```", inline=False)
                    if code and chunk == answer_chunks[-1]:
                        for code_block in code:
                            lang = await AiUtil().detect_language(code_block)
                            embed.add_field(name="Code", value=f"```{lang}{code_block}```", inline=False)
                            if lang == "text":
                                embed.add_field(name="Note", value=f"`Sorry, but we couldn't detect the language of the code block so it doesn't have a syntax highlight.`", inline=False)
                    embed.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Used Tokens : {response['usage']['total_tokens']}")
                    embed.set_image(url="https://i.imgur.com/98NAOch.gif")
                    embed.timestamp = datetime.utcnow()
                    await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(title="ChatGPT - Answer", color=0x00ff00)
                embed.add_field(name="Prompt", value=f"```{prompt}```", inline=False)
                if answer:
                    embed.add_field(name="Response", value=f"```{answer}```", inline=False)
                if code:
                    for code_block in code:
                        lang = await AiUtil().detect_language(code_block)
                        embed.add_field(name="Code", value=f"```{lang}\n{code_block}```", inline=False)
                        if lang == "text":
                            embed.add_field(name="Note", value=f"`Sorry, but we couldn't detect the language of the code block so it doesn't have a syntax highlight.`", inline=False)
                embed.set_footer(text=f"Prompt Tokens: {response['usage']['prompt_tokens']} │ Completion Tokens: {response['usage']['completion_tokens']} │ Used Tokens : {response['usage']['total_tokens']}")
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
            print(e)

    @prompt_command.error
    async def prompt_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(PromptCmd(bot))