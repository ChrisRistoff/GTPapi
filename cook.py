import openai
import configparser
from collections import deque

system_message = """
I need a recipe for ninja foodi multicooker based on the ingredients I give you.
Give me very detailed instructions for cooking the recipe.
if there is a an extra step for a dressing or something do not make a separate list of ingredients for it or a separate list of instructions.
I need a % sign before the title of the recipe.
I need a % sign before the ingredients of the recipe.
use an emoji at the end of each ingredient.
if using the pressure cooker make sure to specify to add water.
"""


def main():
    chat_history = []

    user_input = input("\033[1;31m Ask question: ")
    while user_input != "":

        content = ask_gpt(user_input, chat_history, system_message)

        content = content.split("%")
        title = content[1]
        ingredients = content[2].split("$")
        ingredients = deque(ingredients[0].split("\n"))
        ingredients.popleft()
        ingredients.pop()
        ingredients.pop()

        instructions = deque(content[3].split("\n"))
        instructions.popleft()
        last = instructions.pop()
        instructions.pop()
        instructions.append(last)

        print("TITLE: " + title)

        print("INGREDIENTS:")
        for i in ingredients:
            print(i)

        print("INSTRUCTIONS:")
        for i in instructions:
            print(i)

        # print("\033[1;33m \nAnswer:\n\n", content + "\n")
        user_input = input("\033[1;31m Ask question: ")


def ask_gpt(prompt: str, chat_history: list, system_message: str):
    config = configparser.ConfigParser()
    config.read(".apikey")
    GPT_API = config.get("API", "GPT_API")

    user_prompt = {"role": "user", "content": prompt}

    openai.api_key = GPT_API
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_message},
        *chat_history,
        user_prompt
    ]
    )

    content = response["choices"][0]["message"]["content"]
    chat_history.append(user_prompt)
    chat_history.append({"role": "assistant", "content": content})
    return content

if __name__ == '__main__':
    main()
