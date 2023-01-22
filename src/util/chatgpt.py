import discord
import openai
import json
from .config import Config

class AiUtil():
    def __init__(self):
        self.openai = openai
        self.openai.api_key = Config().openai_key
        
    async def get_prompt(self, prompt: str):
        
        response = self.openai.Completion.create(
            engine=Config().ai_engine,
            prompt=f"Hey give me a response for this: {prompt}",
            temperature=Config().temperature,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        return response.choices[0].text