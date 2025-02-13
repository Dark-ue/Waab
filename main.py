from discord import Intents, Client, Message
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)


intents = Intents.default()
intents.message_content = True #NOQA
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Intents not set up correctly")
        return
    else:
        print (f"Message: {user_message}")
        