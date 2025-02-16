# app/services/pdf_chunk_service.py

import os
import pdfplumber
import nltk
import tiktoken
from typing import List

# Убедитесь, что NLTK-пакет "punkt" установлен
# Например, единожды: nltk.download('punkt')

class PdfChunkService:
    """
    Сервис для:
    1) Извлечения текста из PDF
    2) Деления текста на чанки ~N токенов (не рвать предложения)
    """

    def __init__(self, encoding_name: str = "cl100k_base", default_chunk_size: int = 256):
        """
        :param encoding_name: Название токенизатора (для tiktoken)
        :param default_chunk_size: Число токенов в чанке по умолчанию
        """
        self.encoding_name = encoding_name
        self.default_chunk_size = default_chunk_size

    def read_pdf(self, pdf_path: str) -> str:
        """
        Извлекает текст из всех страниц PDF-файла и склеивает.
        """
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    def split_text_into_chunks(self, text: str, chunk_size: int = None) -> List[str]:
        """
        Делит text на предложения. Каждое предложение в ~N токенов (по умолчанию self.default_chunk_size).
        Если предложение длиннее chunk_size, бьём дополнительно.
        Возвращает список чанков.
        """
        if chunk_size is None:
            chunk_size = self.default_chunk_size

        enc = tiktoken.get_encoding(self.encoding_name)
        sentences = nltk.sent_tokenize(text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # Если предложение само по себе больше chunk_size, режем его
            sub_sentences = self._split_long_sentence(sentence, chunk_size, enc)
            for sub_sent in sub_sentences:
                if not current_chunk:
                    # Если текущий чанк пуст, начинаем с sub_sent
                    current_chunk = sub_sent
                else:
                    combined = current_chunk + " " + sub_sent
                    if self._count_tokens(combined, enc) <= chunk_size:
                        current_chunk = combined
                    else:
                        chunks.append(current_chunk)
                        current_chunk = sub_sent

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _split_long_sentence(self, sentence: str, chunk_size: int, enc) -> List[str]:
        """
        Если одно предложение > chunk_size, режем по токенам на подчанки.
        Иначе возвращаем [sentence].
        """
        tokens = enc.encode(sentence)
        if len(tokens) <= chunk_size:
            return [sentence]

        sub_chunks = []
        for i in range(0, len(tokens), chunk_size):
            sub_tokens = tokens[i : i + chunk_size]
            sub_text = enc.decode(sub_tokens)
            sub_chunks.append(sub_text)
        return sub_chunks

    def _count_tokens(self, text: str, enc) -> int:
        """Подсчёт числа токенов в тексте."""
        return len(enc.encode(text))
