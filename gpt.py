import openai
import argparse
import configparser

system_message = """
I am learning to code, still a beginner. You are my mentor. You will not
answer questions if they are not about coding.
If I ask you a question that is not
related to coding just tell me you can't answer questions not related to coding
Keep the answers as short as you can to get your point across.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="+", type=str,
                        help="The prompt to give to GPT-3")

    chat_history = []

    args = parser.parse_args()
    prompt = " ".join(args.prompt)
    print("\033[1;31m Question:\n\n ", prompt)

    content = ask_gpt(prompt, chat_history, system_message)
    print("\033[1;33m \nAnswer:\n\n", content + "\n")

    user_input = input("\033[1;31m Ask question: ")
    while user_input != "":

        content = ask_gpt(user_input, chat_history, system_message)
        print("\033[1;33m \nAnswer:\n\n", content + "\n")
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
