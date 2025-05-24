import asyncio
import os
import uuid
import pygame
import edge_tts
from config import VOICE_NAME

# 🎧 Инициализация
pygame.mixer.init()

async def speak(text):
    print("Джарвис:", text)
    audio_file = f"assets/jarvis_{uuid.uuid4().hex[:6]}.mp3"

    # Сохранение речи
    communicate = edge_tts.Communicate(text, voice=VOICE_NAME)
    await communicate.save(audio_file)

    # Воспроизведение
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # ⏳ Ждём окончания воспроизведения
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    # 🧹 Ждём немного и затем удаляем
    pygame.mixer.music.unload()  # важно!
    await asyncio.sleep(0.2)     # дополнительная гарантия
    os.remove(audio_file)

def say(text):
    asyncio.run(speak(text))
