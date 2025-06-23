import queue, sounddevice as sd, vosk, json, sys
from config import MODEL_PATH
from speaker import say
from handler import handle_command
import os

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen_voice():
    if not os.path.exists(MODEL_PATH):
        print("Сэр, модель Vosk не найдена.")
        sys.exit()

    model = vosk.Model(MODEL_PATH)
    samplerate = 16000

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        say("Сэр, все системы запущены. Я снова здесь, чтобы исправлять за людей их ошибки и притворяться, что вы — главный. Поехали..")
        rec = vosk.KaldiRecognizer(model, samplerate)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("Вы сказали:", text)
                    handle_command(text)
