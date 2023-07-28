import openai
import elevenlabs
import os

import secrets
import messages
import model


def ask_chat_gpt(newMessage: str):
    # newMessage="Cool es läuft"
    messages.history.append({"role": "user", "content": "Cool es läuft"})

    openai.api_key = secrets.openai
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=model.model + messages.history + [{"role": "user", "content": "Cool es läuft"}],
        temperature=0,
    )
    responseContent = response["choices"][0]["message"]["content"]
    messages.history.append({"role": "system", "content": responseContent})

    with open("messages.py", "w") as f:
        f.write("history=[\n")
        for line in messages.history:
            f.write("    %s,\n" % line)
        f.write("]\n")
        f.close()

    print(responseContent)
    return responseContent

