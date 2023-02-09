import discord
from revChatGPT.Official import AsyncChatbot
import json
from .config import Config
from .message import MsgUtil

class AiUtil():

    def __init__(self):
        self.chatbot = AsyncChatbot(api_key=Config().openai_key)

    async def get_response(self, prompt: str, new_conv: bool = False, conv_id: str = None):

        try:
        
            if new_conv:
                self.chatbot.reset()
            
            response = await self.chatbot.ask(prompt, temperature = 1)
            return response

        except Exception as e:
            print(f"{Fore.RED}>{Fore.WHITE} Error getting prompt: {e}")
            return

    async def get_code_blocks(self, text):
        code_blocks = []
        while "```" in text:
            start = text.index("```")
            end = text.index("```", start + 3)
            code_block = text[start + 3:end].strip()
            code_blocks.append(code_block)
            text = text[:start] + text[end + 3:]
        return code_blocks, text

    async def detect_language(self, code_string):
        try:
            lexer = lexers.guess_lexer(code_string)
            lang = str(lexer.name).lower()
            print("Found language: " + lang)
            return lang
        except Exception as e:
            print("Error detecting language")
            return "text"