import discord
import openai
import json
from .config import Config

class AiUtil():

    def __init__(self):
        self.openai = openai
        self.openai.api_key = Config().openai_key

    async def get_prompt(self, prompt: str, prev: str = None):

        if prev:
            full_prompt = f"Based off this conversation i had with you: {prev}, generate me a prompt for: {prompt}"
        else:
            full_prompt = f"Generate me a prompt for: {prompt}"

        response = self.openai.Completion.create(
            engine=Config().ai_engine,
            prompt=full_prompt,
            temperature=Config().temperature,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response
