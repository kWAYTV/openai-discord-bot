from yaml import SafeLoader
import yaml 
import sys

class Config():
    def __init__(self):
        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.bot_token = self.config["bot_token"]
            self.bot_prefix = self.config["bot_prefix"]
            self.bot_owner = int(self.config["bot_owner_id"])
            self.bot_allowed_role = int(self.config["bot_allowed_role"])
            self.max_chats = int(self.config["max_chats"])
            self.openai_key = self.config["openai_key"]
            self.ai_engine = self.config["ai_engine"]
            self.temperature = float(self.config["temperature"])
            self.db_host = self.config["db_host"]
            self.db_user = self.config["db_user"]
            self.db_pass = self.config["db_pass"]
            self.db_name = self.config["db_name"]