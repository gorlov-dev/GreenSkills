from typing import Optional
from app.web_api.utils.event_dispatcher import event_dispatcher


async def handle_client_message(
    user_id: Optional[int], session_id: str, event: str, payload: dict
):
    """Обработка входящих сообщений от клиента"""
    if event == "ping":
        await event_dispatcher.send(user_id, session_id, "pong", {})

    # elif event == "start_presentation":
    #     await start_presentation(user_id, session_id, payload)

    # elif event == "stop_presentation":
    #     await stop_presentation(user_id, session_id, payload)

    # else:
    #     await event_dispatcher.send(user_id, session_id, "error", {"message": "Неизвестное событие"})
