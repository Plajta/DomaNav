from requests.auth import HTTPDigestAuth
import requests

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