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
