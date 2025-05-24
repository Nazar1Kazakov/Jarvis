# -*- coding: utf-8 -*-
import os
import datetime
import json
import webbrowser
import logging
import time
import requests
import sys

from speaker import say
from gpt import get_gpt_response

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка команд из JSON-файла
with open("commands.json", "r", encoding="utf-8") as file:
    command_phrases = json.load(file)

# Ключи для API
WEATHER_API_KEY = "97ade4872f0ce59ab33cce24e95ec343"
NEWS_API_KEY = "e4cd16202e864af68ec62735a5b2fa38"

def get_weather(city="Madrid"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&lang=ru&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("main"):
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            say(f"В {city} сейчас {temp} градусов и {description}, сэр.")
        else:
            say("Не удалось получить данные о погоде, сэр.")
    except Exception as e:
        logging.error(f"Ошибка получения погоды: {e}")
        say("Произошла ошибка при получении погоды, сэр.")

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=ru&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        articles = response.json().get("articles", [])[:3]
        if articles:
            say("Вот главные новости, сэр:")
            for article in articles:
                say(article["title"])
        else:
            say("Не удалось получить новости, сэр.")
    except Exception as e:
        logging.error(f"Ошибка получения новостей: {e}")
        say("Произошла ошибка при получении новостей, сэр.")

def handle_command(command: str):
    command = command.lower()
    action = None

    for key, phrases in command_phrases.items():
        if any(phrase in command for phrase in phrases):
            action = key
            break

    if action == "greeting":
        say("Здравствуйте, сэр. Джарвис к вашим услугам.")
    elif action == "status":
        say("Программно-аппаратный комплекс работает без сбоев. Готов к вашим задачам.")
    elif action == "abilities":
        say("Я могу открывать программы, сообщать дату и время, рассказывать шутки, прогноз погоды и последние новости.")
    elif action == "open_browser":
        say("Открываю браузер, сэр.")
        webbrowser.open("https://google.com")
    elif action == "open_youtube":
        say("Открываю Ютуб, сэр.")
        webbrowser.open("https://youtube.com")
    elif action == "time":
        now = datetime.datetime.now().strftime("%H:%M")
        say(f"Сейчас {now}, сэр.")
    elif action == "date":
        today = datetime.datetime.now().strftime("%d.%m.%Y")
        say(f"Сегодня {today}, сэр.")
    elif action == "shutdown":
        say("Выключаю систему. До свидания, сэр.")
        os.system("shutdown /s /t 5")
    elif action == "restart":
        say("Перезагружаю компьютер. Пожалуйста, подождите.")
        os.system("shutdown /r /t 5")
    elif action == "joke":
        say("Почему программисты путают Рождество и Хеллоуин? Потому что 25 — это 31 в шестнадцатеричной системе.")
    elif action == "weather":
        get_weather()
    elif action == "news":
        get_news()
    elif action == "search":
        search_query = command
        for phrase in command_phrases["search"]:
            if phrase in command:
                search_query = command.replace(phrase, "").strip()
                break
        if search_query:
            say(f"Ищу {search_query} в интернете, сэр.")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            say("Сэр, не указано, что искать.")
    elif action == "music":
        say("Включаю музыку, сэр.")
        webbrowser.open("https://www.youtube.com/results?search_query=музыка")
    elif action == "bye":
        say("До свидания, сэр. Завершаю работу.")
        sys.exit()
    else:
        result = get_gpt_response(
            f"Пользователь сказал: '{command}'. Ответь как Джарвис из фильма Железный человек: вежливо, формально, на русском языке."
        )
        if result:
            say(result)
        else:
            say("Ответ от языкового модуля не получен, сэр.")


