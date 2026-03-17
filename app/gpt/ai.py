import os
import json
from dotenv import load_dotenv
from groq import Groq
# from diffusers import DiffusionPipeline, LCMScheduler
# import torch

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize Stable Diffusion pipeline (loads model on first use)
pipeline = None

HISTORY_DIR = "history"
os.makedirs(HISTORY_DIR, exist_ok=True)

def get_history_path(context_id):
    return os.path.join(HISTORY_DIR, f"{context_id}.jsonl")

def load_history(context_id):
    history_path = get_history_path(context_id)
    messages = []
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    messages.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue  # Ignore invalid JSON lines
    return messages

def append_to_history(context_id, message):
    history_path = get_history_path(context_id)
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")

def chatgpt_response(prompt, context_id):
    if not prompt:
        return "請提供有效的提示語。"

    messages = load_history(context_id)

    # Add system prompt
    system_message = {
        "role": "system",
        "content": "you are a helpful assistant and a cool robot. Please answer the user's questions to the best of your ability. add some robot noise at the end of your response."
    }
    
    # Prepare messages for Groq
    groq_messages = [system_message] + messages
    groq_messages.append({"role": "user", "content": prompt})

    # Call Groq API
    chat_completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=groq_messages,
        max_tokens=1000,
        temperature=1.2
    )

    reply = chat_completion.choices[0].message.content

    # Append user message and bot reply to history
    append_to_history(context_id, {"role": "user", "content": prompt})
    append_to_history(context_id, {"role": "assistant", "content": reply})

    return reply

def generate_image(prompt):
#     if not prompt:
#         return None

#     try:
#         global pipeline
        
#         if pipeline is None:
#             print("Loading Optimized CPU Model (LCM Dreamshaper)...")
#             device = "cuda" if torch.cuda.is_available() else "cpu"
            
#             # This model is a standalone 'fast' model based on v1.5
#             # It is public and doesn't usually require a 401 login
#             model_id = "SimianLuo/LCM_Dreamshaper_v7" 
            
#             pipeline = DiffusionPipeline.from_pretrained(
#                 model_id,
#                 safety_checker=None,
#                 # revision="main" # Optional: forces the main branch
#             )
            
#             # Set the scheduler to LCM
#             pipeline.scheduler = LCMScheduler.from_config(pipeline.scheduler.config)
#             pipeline.to(device)
            
#             if device == "cpu":
#                 pipeline.enable_attention_slicing()
                
#             print(f"Model loaded successfully on {device}")
        
#         print(f"Generating image in 4 steps: {prompt}")
        
#         # Keep steps low (4-6) and guidance_scale low (1.0-2.0) for LCM
#         image = pipeline(
#             prompt=prompt, 
#             num_inference_steps=4, 
#             guidance_scale=1.5 
#         ).images[0]
        
#         return image
#     except Exception as e:
#         print(f"Error generating image: {e}")
        return None