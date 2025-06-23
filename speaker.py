import asyncio
import os
import uuid
import pygame
import edge_tts
from config import VOICE_NAME

pygame.mixer.init()

is_speaking = False

async def speak(text):
    global is_speaking
    is_speaking = True

    print("Джарвис:", text)
    audio_file = f"assets/jarvis_{uuid.uuid4().hex[:6]}.mp3"

    try:
        # Ускорение речи +20%
        communicate = edge_tts.Communicate(text, voice=VOICE_NAME, rate="+20%")
        await communicate.save(audio_file)

        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        pygame.mixer.music.unload()
        await asyncio.sleep(0.2)
        if os.path.exists(audio_file):
            os.remove(audio_file)

        is_speaking = False

def say(text):
    asyncio.run(speak(text))
