# utils/test_chat_api.py
import streamlit as st
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from utils import get_mongo_client

# Load .env if you're storing secrets there
load_dotenv()

# Get Hugging Face API key from environment
HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    raise ValueError("Hugging Face API key not found. Set HF_API_KEY in your .env file or system env vars.")

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_API_KEY,
)

# Test prompt
stream = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    max_tokens=512,
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
