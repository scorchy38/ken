# # Third-party imports
# import openai
# from fastapi import FastAPI, Form, Depends, Request
# from decouple import config
# # from sqlalchemy.exc import SQLAlchemyError
# # from sqlalchemy.orm import Session

# # Internal imports
# # from models import Conversation, SessionLocal
# from utils import send_message, logger


# app = FastAPI()
# # Set up the OpenAI API client
# openai.api_key = config("OPENAI_API_KEY")
# whatsapp_number = config("TO_NUMBER")

# # Dependency
# # def get_db():
# #     try:
# #         db = SessionLocal()
# #         yield db
# #     finally:
# #         db.close()

# @app.post("/message")
# async def reply(From: str = Form(),Body: str = Form()):
#     # Call the OpenAI API to generate text with GPT-3.5
#     logger.info(From[9:])
#     # response = openai.Completion.create(
#     #     engine="text-davinci-002",
#     #     prompt=Body,
#     #     max_tokens=200,
#     #     n=1,
#     #     stop=None,
#     #     temperature=0.5,
#     # )
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt="Hello! I'm your personal AI health and fitness assistant, here to help you live a healthy and happy life. As a certified health and fitness expert, I have the knowledge and experience to help you achieve your goals.\n\nI can provide you with customized plans and ideas for meals, workout routines, and exercises that fit your lifestyle and goals. Whether you're looking to build muscle, lose weight, or improve your overall fitness, I can create a personalized plan tailored specifically to your needs and preferences.\n\nIf you have any dietary restrictions or preferences, such as vegan, gluten-free, or low-carb, please let me know so that I can take them into consideration when creating your meal plans. Using advanced algorithms and data analysis, I'll create a plan that takes into account your goals, preferences, and current fitness level.\n\nIn addition to physical fitness, I can offer tips and advice on how to improve your mental health and overall well-being. Whether you're looking to manage stress, improve your sleep, or incorporate relaxation techniques into your daily routine, I'm here to help." + Body,
#         temperature=0.7,
#         max_tokens=2966,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     logger.info(response) 
#     # The generated text
#     chat_response = response.choices[0].text.strip()

#     # Store the conversation in the database
  
#     send_message(From[9:], chat_response)
#     return ""


# import openai
# from fastapi import FastAPI, Form, Depends, Request
# from decouple import config
# from utils import send_message, logger

# app = FastAPI()
# openai.api_key = config("OPENAI_API_KEY")
# whatsapp_number = config("TO_NUMBER")

# @app.post("/message")
# async def reply(From: str = Form(), Body: str = Form()):
#     logger.info(From[9:])

#     # Call the OpenAI API to generate text with GPT-3.5 Turbo
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "Hello! I'm your personal AI health and fitness assistant, here to help you live a healthy and happy life. As a certified health and fitness expert, I have the knowledge and experience to help you achieve your goals."
#             },
#             {
#                 "role": "user",
#                 "content": Body
#             }
#         ],
#         temperature=0.7,
#         max_tokens=2966,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     logger.info(response)

#     # The generated text
#     chat_response = response.choices[0]['message']['content'].strip()       

#     # Store the conversation in the database and send the message
#     send_message(From[9:], chat_response)
#     return ""


import openai
import os
from fastapi import FastAPI, Form, Depends, Request
from decouple import config
from utils import send_message, logger

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")
whatsapp_number = config("TO_NUMBER")

conversations = {}

@app.post("/message")
async def reply(From: str = Form(), Body: str = Form()):
    logger.info(From[9:])

    phone_number = From[9:]

    if phone_number not in conversations:
        conversations[phone_number] = [
            {
                "role": "system",
                "content": "Hello! I'm your personal AI health and fitness assistant, here to help you live a healthy and happy life. As a certified health and fitness expert, I have the knowledge and experience to help you achieve your goals."
            }
        ]

    conversations[phone_number].append({"role": "user", "content": Body})

    # Call the OpenAI API to generate text with GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversations[phone_number],
        temperature=0.7,
        max_tokens=2966,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    logger.info(response)

    # The generated text
    chat_response = response.choices[0]['message']['content'].strip()

    # Store the assistant's response in the conversation history
    conversations[phone_number].append({"role": "assistant", "content": chat_response})

    # Send the message
    send_message(phone_number, chat_response)
    return ""
