from app.entities.presentation import PresentationEntity
from app.adapters.db.repositories.slide import SlideRepository
from app.adapters.db.repositories.presentation import PresentationRepository
from app.prompts.llm import LLMService


def scenario_generate_presentation_slides(
    theme: str, relevant_chunks: list[str] = []
) -> str:
    slide_repository = SlideRepository()
    presentation_repository = PresentationRepository()

    """
    Генерация структуры презентации (4 раздела, <=2 подпункта в каждом).
    :param theme: Тема презентации
    :param relevant_chunks: Подходящие тексты, которые могут помочь в генерации
    :return: Строка со структурой или 'Ошибка'
    """
    system_prompt = f"""Ты — эксперт по составлению качественных и интересных презентаций.
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

    llm_service = LLMService()

    # Если вы указали stop_token_ids, преобразуем строку в список int
    if llm_service.stop_token_ids:
        stop_list = []
        for id_str in llm_service.stop_token_ids.split(","):
            id_str = id_str.strip()
            if id_str:
                stop_list.append(int(id_str))
        extra_body["stop_token_ids"] = stop_list

    try:
        response = llm_service.client.chat.completions.create(
            model=llm_service.model_name,
            messages=messages,
            temperature=llm_service.temperature,
            stream=False,
            extra_body=extra_body,
        )
        generated_data = response.choices[0].message.content.strip()

        print(generated_data)
        return generated_data
    except Exception as e:
        logger.error(f"Ошибка при генерации структуры: {e}")
        return "Ошибка"
