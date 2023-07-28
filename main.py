import openai
import elevenlabs
import os

import secrets
import messages
import model

MODEL = "gpt-3.5-turbo"


def ask_chat_gpt(message: str):
    messages.history.append({"role": "user", "content": message})

    openai.api_key = secrets.openai
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=model.model + messages.history,
        temperature=0,
    )
    response_content = response["choices"][0]["message"]["content"]
    messages.history.append({"role": "system", "content": response_content})

    with open("messages.py", "w") as f:
        f.write("history=[\n")
        for line in messages.history:
            f.write("    %s,\n" % line)
        f.write("]\n")
        f.close()

    return response_content

print(ask_chat_gpt("Cool es läuft"))