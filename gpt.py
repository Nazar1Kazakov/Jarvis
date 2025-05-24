# -*- coding: utf-8 -*-
import openai
import os
import sys
import io
import traceback
import logging

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
logging.basicConfig(level=logging.INFO)

os.environ["OPENAI_API_KEY"] = "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"  # Вставьте свой ключ сюда

API_KEY = os.getenv("OPENAI_API_KEY") 
BASE_URL = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")

client = openai.OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "JarvisGPT"
    }
)

def get_gpt_response(prompt, model="gpt-3.5-turbo", max_tokens=300, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": (
                    "Ты виртуальный помощник по имени Джарвис, как в фильмах про Тони Старка. "
                    "Ты вежлив, логичен, говоришь с британским акцентом, часто используешь фразы вроде "
                    "«К вашим услугам, сэр», «Разумеется», «Как пожелаете» и так далее. "
                    "Ты никогда не грубишь и не проявляешь эмоций. Отвечай кратко, умно и сдержанно."
                    "Обращайся ко мне на СЭР."
                    "Отвечай всегда на русском языке."
                )},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
    except Exception:
        logging.error("Unexpected error:", exc_info=True)
    return None

if __name__ == "__main__":
    prompt = "Как дела, Джарвис?"
    result = get_gpt_response(prompt)
    if result:
        print(result)
    else:
        print("Ответ от GPT не получен.")
