from requests.auth import HTTPDigestAuth
import requests
from pydub import AudioSegment
from pydub.playback import play

ROOT = "https://services.speechtech.cz/tts/v4"
USERNAME = "aimtechackathon"
PASSWORD = "lu7Eabuu7E"

def SpeechToText():
    params = {
        'format': 'plaintext',
    }

    with open('src/SpeechRec/out/output.mp3', 'rb') as f:
        data = f.read()

    response = requests.post('https://uwebasr.zcu.cz/api/v1/CLARIN_ASR/CZ', params=params, data=data)
    response.raise_for_status()
    
    print(response.text)

def TextToSpeech(text):
    text = text.replace(" ", ".")

    r = requests.get(ROOT+"/synth",
                 data={"engine": "Iva30",  # Iva30, Jan30
                       "text": text,
                       "format": "mp3",
                       },
                  auth=HTTPDigestAuth(USERNAME, PASSWORD),
                 )
    r.raise_for_status()

    with open("output.mp3", "wb") as fw:
        fw.write(r.content)

    audio = AudioSegment.from_mp3("output.mp3")
    play(audio)

TextToSpeech()
SpeechToText()