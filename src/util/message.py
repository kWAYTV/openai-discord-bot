import discord
import json
from .config import Config

class MsgUtil():

    def __init__(self):

        def split_string_into_chunks(string, chunk_size):
            chunks = []# Create an empty list to store the chunks
            while len(string) > 0:# Use a while loop to iterate over the string
                chunk = string[:chunk_size]# Get the first chunk_size characters from the string
                chunks.append(chunk)# Add the chunk to the list of chunks
                string = string[chunk_size:]# Remove the chunk from the original string
            return chunks # Return the list of chunks
