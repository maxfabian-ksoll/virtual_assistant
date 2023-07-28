import openai
import requests
from elevenlabs import clone, generate, set_api_key, save
from time import time

import pathlib
import secrets
import messages
import model

CREATE_CLIP_URL = "https://api.d-id.com/clips"
GET_CLIP_URL = "https://api.d-id.com/clips"
UPLOAD_AUDIO = "https://api.d-id.com/audios"
DID_KEY = secrets.did
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

def generate_video(path_to_audio: str):
    # print(create_video_from_audio("https://www.lightbulblanguages.co.uk/resources/ge-audio/beach-german.mp3"))
    audio_headers = {
        "accept": "application/json",
        "content-type": "multipart/form-data",
        "authorization": "Basic "+DID_KEY
    }
    response = requests.post(UPLOAD_AUDIO, headers=audio_headers).json()
    print(response)
    audio_url=response["url"]
    headers = {"Authorization": "Basic "+DID_KEY}
    create_clip = {
        "script": {
            "type": "audio",
            "audio_url": audio_url
        },
        "presenter_id": "amy-jcwCkr1grs",
        "driver_id": "uM00QMwJ9x"
    }
    response = requests.post(CREATE_CLIP_URL, headers=headers, json=create_clip).json()
    print(response)
    clip_id = response["id"]
    clip = requests.get(GET_CLIP_URL + "/" + clip_id, headers=headers).json()
    print(clip)
    return clip["result_url"]
