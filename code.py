import os  #Импоритурем библиотеки

from dotenv import load_dotenv #Чтобы читал файлы из .env

from google import genai #Импортируем genai(ai)

from google.genai import types

import time

from google.genai import errors

load_dotenv() # Читаем файл из .env
api_key = os.getenv("GEMINI_API_KEY") # Создаем переменную и кладем название ключа(поиск по значению по типу Dict)



client = genai.Client(api_key = api_key)


def ask_model(history):
    for attemp in range(3):
        try:
            response = client.models.generate_content(
                model = "gemini-3.5-flash-lite",
                contents=history,
                config = types.GenerateContentConfig(
                    system_instruction= "You are friendly restaruant assistant",
                    temperature=0.5
                ),
            )
            return response.text
        except errors.ServerError:
            print(f"Сервер перегружен, попытка {attemp +1} из 3")
            time.sleep(2)
    return None

history = []

while True:
    user_text = input("Вводит пользователь текст")
    if user_text.strip() == "Exit":
        print("Рад был поговорить, буду ждать вас")
        break
    
    history.append(types.Content(role="user", parts=[types.Part(text = user_text)]))

    answear = ask_model(history)
    if answear is None:
        print("Сервис перегружен")
        history.pop()
        continue

    print("Бот", answear)
    history.append(types.Content(role="model",parts = [types.Part(text = answear)]))