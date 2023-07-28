import openai
from elevenlabs import clone, generate, set_api_key, save
from time import time

import pathlib
import secrets
import messages
import model

MODEL = "gpt-3.5-turbo"
openai.api_key = secrets.openai
set_api_key(secrets.elevenlabs)


def ask_chat_gpt(message: str) -> str:
    messages.history.append({"role": "user", "content": message})

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


def clone_voice(name: str, description, path_to_voices: list[pathlib.Path]):
    voice = clone(
        name=name,
        description=description,
        label={"gender": "male", "age": "30", "accent": "german"},
        files=path_to_voices)
    return voice


def generate_audio(message: str):
    audio = generate(text=message, voice="Isa", model="eleven_multilingual_v1")
    timestamp = time()
    path = pathlib.Path(rf"C:\Users\ksoll\Documents\GitProjects\virtual_assistant\audio_files\{timestamp}.mp3")
    save(audio, str(path.absolute()))
    return path, audio


def generate_video(audio_path):
    pass
