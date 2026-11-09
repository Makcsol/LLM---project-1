import os
from google import genai
from google.genai import errors
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import ValidationError


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


menu_catogories = {1:"Первые блюда", 2: "Основные блюда", 3: "Десерты"}

class MenuItemId(BaseModel):

    name : str
    price : float
    category_id : int
    time_preparation_dish : int
    is_available : bool

def dish_function(description):
    responce = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = description,
        config = types.GenerateContentConfig(
            response_mime_type = "application/json",
            response_schema = MenuItemId,
            system_instruction=f"Hello, you are my personal assistant in the category 'Restaurant Menu'. Respond in JSON format and find the category_id for the dish the user enters using these categories: {menu_catogories}. And don't switch name for dish.",
            temperature=0.2
        ))
    
    try:
        item = MenuItemId.model_validate_json(responce.text)
        return item
    except ValidationError:
        print("Not correct text in data")
        return None


description = input("Введите текст согласно описанию шаблона : ")
results_2 = dish_function(description)
print(results_2)








    


    