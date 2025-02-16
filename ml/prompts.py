from loguru import logger
import openai
from dotenv import load_dotenv
from openai import OpenAI
import os
model_url='http://localhost:8000/v1'
model_name='t-tech/T-lite-it-1.0'
open_api_key='EMPTY'
logger.add("processing.log", rotation="10 MB", level="INFO")


class ChatBot():
    def __init__(self, model_url=model_url, model=model_name,open_api_key=open_api_key, temp=0.4, stop_token_ids=''):
        self.model_url= model_url
        self.model=model
        self.temp=temp
        self.stop_token_ids=stop_token_ids
        self.open_api_key = open_api_key
        self.client= OpenAI(api_key= open_api_key, base_url= self.model_url)
    
    def generate_structure(self, theme: str, relevants_chunks: list) -> str:
        history_openai_format = [{
            "role": "system",
            "content": """Ты — эксперт по составлению качественных и интересных презентаций.
            Твоя главная задача: составить качественную структуру для будущей презентации на определенную тему.
            Презентация должна содержать ровно 4 раздела.
            В каждом разделе должно быть не более 2 подпунктов
            В ответе ты должен выводить лишь структуру.
            Формат вывода:
            - Тема презентации: [Указать тему].
            1. [Название раздела]
               - [Подпункт 1]
               - [Подпункт 2]
            2. [Название раздела]
               - [Подпункт 1]
               - [Подпункт 2]
            3. [Название раздела]
               - [Подпункт 1]
               - [Подпункт 2]
            """
        }]
        user_prompt = f"Подходящие релевантные тексты:\n" + "\n".join(
            relevants_chunks) + (f"Проанализируй данные тексты и сформируй разделы и интересные пункты для презентации на тему {theme}")
        history_openai_format.append({"role": "user", "content": user_prompt})
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=history_openai_format,
                temperature=self.temp,
                stream=False,
                extra_body={
                    'repetition_penalty': 1,
                    "max_tokens": 512,
                    'stop_token_ids': [
                        int(id.strip()) for id in self.stop_token_ids.split(',')
                        if id.strip()
                    ] if self.stop_token_ids else []
                })
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")
            return "Ошибка"

    def generate_text_section(self, section: str, relevant_chunks: list) -> str:
        history_openai_format = [{
            "role": "system",
            "content": f"""Ты — эксперт по составлению качественных и интересных презентаций. 
            Твоя задача написать краткое эссе на определенную тему.
            Для составления текста используй также дополнительные подсказки: {''.join(relevant_chunks)}
            Если подсказок нет или они плохие, то игнорируй их. 
            Выдавай строго не больше 3 предложений.
            После темы раздела сразу пиши по теме. 
            Формат вывода:
            [Название раздела]
             - [Текст раздела]
            """
        }]
        user_prompt = f"Тема раздела: {section}"
        history_openai_format.append({"role": "user", "content": user_prompt})
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=history_openai_format,
                temperature=self.temp,
                stream=False,
                extra_body={
                    'repetition_penalty': 1,
                    "max_tokens": 256,
                    'stop_token_ids': [
                        int(id.strip()) for id in self.stop_token_ids.split(',')
                        if id.strip()
                    ] if self.stop_token_ids else []
                })
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")
            return "Ошибка"

chat = ChatBot()
