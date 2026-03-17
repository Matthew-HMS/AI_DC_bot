import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from io import BytesIO
from dotenv import load_dotenv
from app.gpt.ai import chatgpt_response, generate_image

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

# 1. Setup Bot with necessary Intents
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # This registers your slash commands with Discord
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

bot = MyBot()

# 2. The /image Slash Command
@bot.tree.command(name="image", description="Generate an image from a prompt")
@app_commands.describe(prompt="What should I generate?")
async def image(interaction: discord.Interaction, prompt: str):
    # This "defers" the response, showing "Bot is thinking..." 
    # This prevents the "interaction failed" error if generation takes > 3 seconds.
    await interaction.response.defer()

    try:
        # Run the blocking image generation in a thread
        image_data = await asyncio.to_thread(generate_image, prompt)

        if image_data:
            image_bytes = BytesIO()
            image_data.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            file = discord.File(image_bytes, filename="generated.png")
            
            # Use followup.send because we deferred earlier
            await interaction.followup.send(content=f"**Prompt:** {prompt}", file=file)
        else:
            await interaction.followup.send("Failed to generate image.")
    except Exception as e:
        await interaction.followup.send(f"This function is currently colosed !!")
        await interaction.followup.send(f"An error occurred: {e}")

# 3. The /ai Slash Command
@bot.tree.command(name="ai", description="Chat with the AI")
@app_commands.describe(message="Your question for the AI")
async def ai(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    
    context_id = str(interaction.guild_id if interaction.guild else interaction.user.id)
    
    try:
        response = await asyncio.to_thread(chatgpt_response, message, context_id)
        await interaction.followup.send(response)
    except Exception as e:
        await interaction.followup.send(f"Chat error: {e}")

bot.run(discord_token)