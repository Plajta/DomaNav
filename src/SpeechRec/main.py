from requests.auth import HTTPDigestAuth
import requests
from pydub import AudioSegment
from pydub.playback import play
import whisper

ROOT = "https://services.speechtech.cz/tts/v4"
USERNAME = "aimtechackathon"
PASSWORD = "lu7Eabuu7E"

def SpeechToText():
    model = whisper.load_model("small")
    audio = whisper.load_audio("src/SpeechRec/out/output.mp3")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language = "cs", fp16 = False)

    result = whisper.decode(model, mel, options)
    print(result.text)

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

    with open("src/SpeechRec/out/output.mp3", "wb") as fw:
        fw.write(r.content)

    audio = AudioSegment.from_mp3("src/SpeechRec/out/output.mp3")
    play(audio)

TextToSpeech()
SpeechToText()