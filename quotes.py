import openai
import configparser
from collections import deque

system_message = """
"""


def main():
    prompt = """Give me a random quote. Do not put it in quotes but put a % symbol between the quote and the author.
    Example: The best way to predict the future is to invent it. %Alan Kay
    """
    content = ask_gpt(prompt)

    content = content.split("%")
    quote = content[0]
    author = content[1]

    print('"' + quote + '"')
    print("-" + author)

def ask_gpt(prompt: str):
    config = configparser.ConfigParser()
    config.read(".apikey")
    GPT_API = config.get("API", "GPT_API")

    user_prompt = {"role": "user", "content": prompt}

    openai.api_key = GPT_API
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        user_prompt
    ]
    )

    content = response["choices"][0]["message"]["content"]
    return content

if __name__ == '__main__':
    main()
