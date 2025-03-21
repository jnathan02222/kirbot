from transformers import pipeline
import discord
import os
from dotenv import load_dotenv
load_dotenv()

generator = pipeline('text-generation', model='./result-medium', tokenizer='gpt2', max_new_tokens=128, truncation=True)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

impersonate = "darren2427"


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    prompt = ""
    async for msg in message.channel.history(limit=20):  # Adjust the limit as needed
        prompt += f"{impersonate if msg.author == client.user else msg.author}: {msg.content}\n"

    result = generator(prompt + f"{impersonate}: ")[0]['generated_text'][len(prompt):]
    generated_one = False
    print(result)
    for msg in result.split("\n"):
        author = msg[:msg.find(":")]
        content = msg[msg.find(":")+1:].strip()
        if(author != impersonate and generated_one):
            break
        if content != "" and content.find("@") == -1:
            await message.channel.send(content)
            generated_one = True
        

client.run(os.getenv('BOT_TOKEN'))