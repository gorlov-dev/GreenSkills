# app/services/embedding_service.py

from sentence_transformers import SentenceTransformer
from typing import List
from loguru import logger


class EmbeddingService:
    """
    Сервис для преобразования текста в эмбеддинги (векторное представление)
    с помощью SentenceTransformer.
    """

    def __init__(self, model_name: str = "BAAI/bge-m3"):
        """
        :param model_name: Название модели из Hugging Face (например "BAAI/bge-m3")
        """
        logger.info(f"Инициализируем SentenceTransformer c моделью: {model_name}")
        self.model = SentenceTransformer(model_name)

    def encode_text(self, text: str) -> List[float]:
        """
        Кодирует один текст в вектор (float-список).
        """
        embedding = self.model.encode(text)
        return embedding.tolist()

    def encode_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Кодирует несколько текстов (чанков) в список векторов.
        """
        embeddings = self.model.encode(texts)
        # Преобразуем в list of lists (numpy → python)
        return [emb.tolist() for emb in embeddings]
