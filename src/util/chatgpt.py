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