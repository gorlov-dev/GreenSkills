
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
# Импортируем ваш класс ChatBot из chat_bot.py
from prompts import ChatBot

# Создаём модели запросов
class GenerateStructureRequest(BaseModel):
    theme: str
    relevants_chunks: List[str]

class GenerateTextSectionRequest(BaseModel):
    section: str
    relevant_chunks: List[str]

app = FastAPI()

# Инициализируем экземпляр бота (укажите нужные реальные значения)
chatbot = ChatBot()
@app.get("/")
def read_root():
    return {"message": "Welcome to ChatBot API! Use /docs for documentation."}
@app.post("/generate_structure")
def generate_structure(request: GenerateStructureRequest):
    """
    Хендлер, который принимает тему и список релевантных текстов,
    и возвращает сгенерированную структуру презентации.
    """
    result = chatbot.generate_structure(
        theme=request.theme,
        relevants_chunks=request.relevants_chunks
    )
    return {"result": result}

@app.post("/generate_text_section")
def generate_text_section(request: GenerateTextSectionRequest):
    """
    Хендлер, который принимает название раздела и список релевантных текстов,
    и возвращает сгенерированный текст раздела.
    """
    result = chatbot.generate_text_section(
        section=request.section,
        relevant_chunks=request.relevant_chunks
    )
    return {"result": result}
