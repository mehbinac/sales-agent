# backend/main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import requests
from config import REMOTE_LLM_URL

def ask_llm(message: str) -> str:
    response = requests.post(
        REMOTE_LLM_URL,
        json={"message": message},
        timeout=60
    )
    response.raise_for_status()
    return response.json()["response"]


if __name__ == "__main__":
    try:
        ask_llm("Hello")
        print("Connected to remote LLM successfully.")
    except Exception as e:
        print(f"Failed to connect to remote LLM: {e}")
        sys.exit(1)
    print("Type your message (type 'exit' to quit):")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting.")
            break

        try:
            reply = ask_llm(user_input)
            print("LLM:", reply)
        except Exception as e:
            print("Error talking to LLM:", e)
