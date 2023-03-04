import pyaudio
import numpy as np
import whisper

channel = 1
frame_rate = 44100
record_seconds = 10
audio_format = pyaudio.paInt16
chunk = 4096
model = whisper.load_model("medium")

p = pyaudio.PyAudio()

stream = p.open(
    format=audio_format,
    channels=channel,
    rate=frame_rate,
    input=True,
    input_device_index=20,
    frames_per_buffer=chunk,
)

frames = []
listening = True

while listening:
    data = stream.read(chunk)
    frames.append(data)
    if len(frames) >= frame_rate * record_seconds / chunk:
        audio = np.frombuffer(data, np.int16).astype(np.float32) * (1 / 32768.0)
        
        #options = whisper.DecodingOptions(language = "cs", fp16 = False)

        transcription = model.transcribe(audio)

        #result = whisper.decode(model, mel, options)
        print(transcription["text"])
        
        frames = []

print("Stop")
stream.stop_stream()
stream.close()
p.terminate()