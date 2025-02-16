# app/services/llm_service.py

import os
from loguru import logger
from openai import OpenAI

class LLMService:
    """
    Сервис для взаимодействия с LLM-моделью через OpenAI-like API (vllm).
    Позволяет генерировать структуру презентации и текст для разделов.
    """

    def __init__(
        self,
        model_url: str = "http://127.0.0.1:8000/v1",
        model_name: str = "t-tech/T-lite-it-1.0",
        open_api_key: str = "EMPTY",
        temperature: float = 0.4,
        stop_token_ids: str = "",
    ):
        """
        :param model_url:     URL, где поднят vllm/OpenAI-совместимый сервер (e.g. http://127.0.0.1:8000/v1)
        :param model_name:    Название модели (e.g. "t-tech/T-lite-it-1.0")
        :param open_api_key:  Ключ авторизации (если есть, в vllm обычно "EMPTY")
        :param temperature:   'temperature' для генерации
        :param stop_token_ids: Строка с ID токенов, например '50256,50257', если нужно остановить вывод
        """
        self.model_url = model_url
        self.model_name = model_name
        self.open_api_key = open_api_key
        self.temperature = temperature
        self.stop_token_ids = stop_token_ids

        # Инициализируем клиента (openai.OpenAI), но с кастомным base_url = self.model_url
        # Это нужно, чтобы слать запросы в ваш vllm-контейнер
        self.client = OpenAI(api_key=open_api_key, base_url=model_url)

        # Настраиваем логгер (если нужно — в другом месте).
        logger.add("processing.log", rotation="10 MB", level="INFO")

    def generate_structure(self, theme: str, relevant_chunks: list[str]) -> str:
        """
        Генерация структуры презентации (4 раздела, <=2 подпункта в каждом).
        :param theme: Тема презентации
        :param relevant_chunks: Подходящие тексты, которые могут помочь в генерации
        :return: Строка со структурой или 'Ошибка'
        """
        system_prompt = """Ты — эксперт по составлению качественных и интересных презентаций.
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
4. [Название раздела]
   - [Подпункт 1]
   - [Подпункт 2]
"""

        # Формируем сообщение "user"
        user_prompt = (
            "Подходящие релевантные тексты:\n"
            + "\n".join(relevant_chunks)
            + f"\nПроанализируй данные тексты и сформируй разделы и интересные пункты "
            f"для презентации на тему: {theme}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Собираем параметры для запроса
        extra_body = {
            "repetition_penalty": 1,
            "max_tokens": 512,
        }

        # Если вы указали stop_token_ids, преобразуем строку в список int
        if self.stop_token_ids:
            stop_list = []
            for id_str in self.stop_token_ids.split(","):
                id_str = id_str.strip()
                if id_str:
                    stop_list.append(int(id_str))
            extra_body["stop_token_ids"] = stop_list

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                stream=False,
                extra_body=extra_body,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Ошибка при генерации структуры: {e}")
            return "Ошибка"

    def generate_text_section(self, section: str, relevant_chunks: list[str]) -> str:
        """
        Генерация краткого (<=3 предложения) текста по теме раздела.
        :param section: Название (тема) раздела
        :param relevant_chunks: Подсказки или дополнительные тексты
        :return: Строка результата или 'Ошибка'
        """
        system_prompt = f"""Ты — эксперт по составлению качественных и интересных презентаций.
Твоя задача написать краткое эссе на определенную тему.
Для составления текста используй также дополнительные подсказки: {''.join(relevant_chunks)}
Если подсказок нет или они плохие, то игнорируй их.
Выдавай строго не больше 3 предложений.
После темы раздела сразу пиши по теме.
Формат вывода:
[Название раздела]
 - [Текст раздела]
"""

        user_prompt = f"Тема раздела: {section}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        extra_body = {
            "repetition_penalty": 1,
            "max_tokens": 256,
        }

        if self.stop_token_ids:
            stop_list = []
            for id_str in self.stop_token_ids.split(","):
                id_str = id_str.strip()
                if id_str:
                    stop_list.append(int(id_str))
            extra_body["stop_token_ids"] = stop_list

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                stream=False,
                extra_body=extra_body,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Ошибка при генерации текста для раздела: {e}")
            return "Ошибка"

# app/services/llm_service.py

def summarize_text_chunk(self, chunk_text: str) -> str:
    """
    Суммаризация одного чанка текста (в 1-3 предложениях).
    """
    system_prompt = """Ты — эксперт, который кратко пересказывает текст.
Ответ должен содержать не более 3 предложений, суммируя суть полученного текста.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Текст для суммаризации:\n{chunk_text}"
        },
    ]

    extra_body = {
        "repetition_penalty": 1,
        "max_tokens": 256,
    }

    if self.stop_token_ids:
        stop_list = []
        for id_str in self.stop_token_ids.split(","):
            id_str = id_str.strip()
            if id_str:
                stop_list.append(int(id_str))
        extra_body["stop_token_ids"] = stop_list

    try:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            stream=False,
            extra_body=extra_body,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка при суммаризации чанка: {e}")
        return "Ошибка"


llm_service = LLMService(
    model_url="http://127.0.0.1:8000/v1",
    model_name="t-tech/T-lite-it-1.0",
    open_api_key="EMPTY",
    temperature=0.4,
    stop_token_ids="")