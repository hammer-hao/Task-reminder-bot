import requests
from dotenv import load_dotenv
import os
import discord
import openai
from langdetect import detect

load_dotenv()
APIkey=os.getenv('APIKEY')
token=os.getenv('DISCORDTOKEN')

Chatkey=('Bearer '+APIkey)
headers = {
    'Authorization': Chatkey,
}

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if detect(message.content)!='en':
        prompt=(message.content+'. Respond to the previous sentence while subtly hinting at the ongoing game development project in a sarcastic manner')
        json_data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'temperature': 1,
        'max_tokens': 100,
        }
        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data, timeout=5)
        if response.status_code==200:
            textresponse=response.json()['choices'][0]['text'].strip().splitlines()[-1]
            print('sending')
            await message.channel.send(textresponse)
    elif detect(message.content)=='en':
        prompt=('Respond to this sentence while subtly hinting at the ongoing game development project in a sarcastic manner: '+message.content)
        json_data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'temperature': 1,
        'max_tokens': 100,
        }
        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data, timeout=5)
        if response.status_code==200:
            textresponse=response.json()['choices'][0]['text'].strip().splitlines()[-1]
            print('sending')
            await message.channel.send(textresponse)

client.run(token)