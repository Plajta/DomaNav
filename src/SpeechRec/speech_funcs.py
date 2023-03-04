from requests.auth import HTTPDigestAuth
import requests
import playsound
import pyaudio
import speech_recognition as sr

Recognizer = sr.Recognizer()
Pyaudio = pyaudio.PyAudio()

#some info
info = Pyaudio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

ROOT = "https://services.speechtech.cz/tts/v4"
USERNAME = "aimtechackathon"
PASSWORD = "lu7Eabuu7E"

#
# FUNCTIONS
#
def SpeechToText(source):
    Stream = Recognizer.listen(source, phrase_time_limit=4)

    Command_args = []
    try:
        Command_args = Recognizer.recognize_google(Stream, language="cs")
        if type(Command_args) == str:
            Command_args = Command_args.split()
    except sr.UnknownValueError:
        print("cannot read the stream")
        Command_args = []

    return Command_args 

def TextToSpeech(text):
    text = text.replace(" ", ". ")

    r = requests.get(ROOT+"/synth",
                 data={"engine": "Iva30",  # Iva30, Jan30
                       "text": text,
                       "format": "mp3",
                       "stream": 1
                       },
                  auth=HTTPDigestAuth(USERNAME, PASSWORD),
                )
    r.raise_for_status()

    with open("src/SpeechRec/out/output.mp3", "wb") as fw:
        fw.write(r.content)

    playsound.playsound("src/SpeechRec/out/output.mp3")

def PlaySpeech(audio_name):
    playsound.playsound("src/SpeechRec/out/" + audio_name + ".mp3")