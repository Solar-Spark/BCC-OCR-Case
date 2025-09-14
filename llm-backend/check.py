import os
from dotenv import load_dotenv
from openai import OpenAI

# 🔑 Load token from .env file
load_dotenv()

token = os.getenv("GITHUB_API_KEY")
if not token:
    raise ValueError("❌ GITHUB_API_KEY not found in .env file")

# 🌐 GitHub Models endpoint
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-5"  # Example model

# Initialize client
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# 📋 List available models
print("🔍 Fetching available models...\n")

try:
    models = client.models.list()
    for m in models.data:
        print(f"- {m.id}")
except Exception as e:
    print("⚠️ Error while fetching models:", e)
