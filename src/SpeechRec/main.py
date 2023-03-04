from requests.auth import HTTPDigestAuth
import requests
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import pyaudio
import whisper
import speech_recognition as sr
import io

ROOT = "https://services.speechtech.cz/tts/v4"
USERNAME = "aimtechackathon"
PASSWORD = "lu7Eabuu7E"

Recognizer = sr.Recognizer()

def SpeechToText():
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
    """
    model = whisper.load_model("small")
    audio = whisper.load_audio("src/SpeechRec/out/output.mp3")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language = "cs", fp16 = False)

    result = whisper.decode(model, mel, options)
    print(result.text)
    """

    Stream = Recognizer.listen(source)

    Command_args = []
    try:
        Command_args = Recognizer.recognize_google(Stream, language="cs")
        if type(Command_args) == str:
            Command_args = Command_args.split()
            print(Command_args)
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

    audio = AudioSegment.from_mp3("src/SpeechRec/out/output.mp3")
    play(audio)

Pyaudio = pyaudio.PyAudio()

#TextToSpeech("Jdu do ložnice")
#SpeechToText()

#some info
info = Pyaudio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (Pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", Pyaudio.get_device_info_by_host_api_device_index(0, i).get('name'))

with sr.Microphone() as source:
    Recognizer.adjust_for_ambient_noise(source)
    while True:
        Commands = SpeechToText()
        if len(Commands) != 0:
            pass
