from requests.auth import HTTPDigestAuth
import requests
from pydub import AudioSegment
from pydub.playback import play

ROOT = "https://services.speechtech.cz/tts/v4"
USERNAME = "aimtechackathon"
PASSWORD = "lu7Eabuu7E"

def SpeechToText():
    pass

def TextToSpeech():
    r = requests.get(ROOT+"/synth",
                 data={"engine": "Iva30",  # Iva30, Jan30
                       "text": "Vítejte a syntetizujte",
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