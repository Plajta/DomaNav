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
    """
    params = {
        'format': 'plaintext',
    }

    if mode == "mp3":
        with open('src/SpeechRec/out/output.mp3', 'rb') as f:
            data = f.read()

    response = requests.post('https://uwebasr.zcu.cz/api/v1/CLARIN_ASR/CZ', params=params, data=data)
    response.raise_for_status()
    
    print(response.text)
    """
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

#
# MAIN
#
def Speechmain(callback = None):
    #
    # VARIABLES
    #
    Command_buffer = []

    Desired_Data = [["postel", "posteli", "postelí", "postele"], #ano, všechno jsem to vyskloňoval...
                    ["stůl", "stolu", "stolem"],
                    ["křeslo", "křesla", "křeslu", "křeslem"],
                    ["televize", "televizi", "televizí"],
                    ["záchod", "záchodu", "záchodě", "záchodem"],
                    ["lednice", "lednici", "lednicí"],
                    ["kuchyň", "kuchyně", "kuchyní", "kuchyni"],
                    ["koupelna", "koupelny", "koupelně", "koupelnu", "koupelnou"],
                    ["ložnice", "ložnici", "ložnicí"]]


    for i in range(0, numdevices):
        if (Pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", Pyaudio.get_device_info_by_host_api_device_index(0, i).get('name'))

    # if "začal se pohybovat:"
    #
    #
    PlaySpeech("KamJdes")

    with sr.Microphone() as source:
        Recognizer.adjust_for_ambient_noise(source)
        while True:
            Commands = SpeechToText(source)

            if len(Commands) == 0: #skipoing empty command
                continue

            Command_buffer.extend(Commands)
            print(Command_buffer)
            #nějaké vyhodnocení a nalezení místnosti
            for y_data in Desired_Data:
                for data in y_data:
                    if data in Command_buffer: #We found desired word!
                        
                        #callback()
                        Command_buffer = []
