from dotenv import load_dotenv
import discord
import os
from app.gpt.ai import chatgpt_response, generate_image

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}!")

    async def on_message(self, message):
        print(message.content)
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        if message.content.startswith("/image"):
            prompt = message.content[len("/image"):].strip()
            if not prompt:
                await message.channel.send("Please provide a prompt for the image generation.")
                return

            await message.channel.send("Generating image, please wait...")
            image_url = generate_image(prompt)
            if image_url:
                await message.channel.send(image_url)
            else:
                await message.channel.send("Failed to generate image. Please try again later.")
        
        else: 
            command, user_message = None, None

            for text in ["/ai", "/bot", "/chatgpt"]:
                if message.content.startswith(text):
                    command = message.content.split(" ")[0]
                    user_message = message.content.replace(text, "").strip()
                    print(command, user_message)

            if command in ['/ai', '/bot', '/chatgpt']:
                # Determine context ID based on message type
                if message.guild is None:
                    # Direct Message
                    context_id = str(message.author.id)
                else:
                    # Message in a server channel
                    context_id = str(message.guild.id)

                bot_response = chatgpt_response(prompt=user_message, context_id=context_id)
                await message.channel.send(f"{bot_response}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)