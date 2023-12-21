import discord
from discord import app_commands
from typing import List
import os
from os.path import join, dirname
from dotenv import load_dotenv

#インテントの設定
intent = discord.Intents.default()
intent.message_content = True
client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
server_id = os.environ.get("SERVER_ID")
emoji:List[discord.Emoji] = [
    "1️⃣", 
    "2️⃣", 
    "3️⃣", 
    "4️⃣", 
    "5️⃣", 
    "6️⃣", 
    "7️⃣", 
    "8️⃣",
    "9️⃣"]
choice_max = 4


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print("get on ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#コマンド
@tree.command(
    name="vote",
    description="create new vote"
)
@discord.app_commands.guilds(server_id)
async def vote(ctx: discord.Interaction, question: str, choices: str):
    choice_list:list = choices.split(' ')
    while (len(choice_list) < choice_max):
        choice_list.append("")

    #メッセージの作成と送信
    msg = f">>> {question}\n"
    for i in range(choice_max):
        if choice_list[i] != "":
            msg = msg+f"{i+1}: {choice_list[i]}\n"
    await ctx.response.send_message(msg)
    response: discord.InteractionMessage = await ctx.original_response()

    #メッセージにリアクションをつける
    for i in range(choice_max):
        if choice_list[i] != "":
            await response.add_reaction(emoji[i])
    
client.run(DISCORD_TOKEN)