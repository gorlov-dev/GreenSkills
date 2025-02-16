from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.web_api.utils.event_dispatcher import event_dispatcher
from app.web_api.utils.token_helper import TokenHelper
from app.web_api.routes.websocket.handler import handle_client_message

ws_router = APIRouter(prefix="/ws", tags=["WebSocket"])


async def get_user_from_token(token: str) -> Optional[int]:
    """Проверка токена и получение user_id"""
    if not token:
        return None

    try:
        payload = TokenHelper.decode(token)
        return payload.get("user_id")
    except Exception:
        return None


@ws_router.websocket("/{session_id}")
async def websocket_connection(websocket: WebSocket, session_id: str):
    """WebSocket обработчик с авторизацией после подключения"""
    user_id: Optional[int] = None  # По умолчанию гость

    try:
        await websocket.accept()
        await event_dispatcher.connect(user_id, session_id, websocket)

        while True:
            try:
                data = await websocket.receive_json()
                event = data.get("event")
                payload = data.get("data", {})

                if event == "authenticate":
                    token = payload.get("token")
                    user_id = await get_user_from_token(token)

                    if user_id:
                        await event_dispatcher.authorize_connection(user_id, session_id)
                        await event_dispatcher.send(
                            user_id,
                            session_id,
                            "authenticated",
                            {"message": "Вы авторизованы!"},
                        )
                    else:
                        await event_dispatcher.send(
                            None, session_id, "error", {"message": "Ошибка авторизации"}
                        )

                else:
                    await handle_client_message(user_id, session_id, event, payload)

            except WebSocketDisconnect:
                break
    finally:
        await event_dispatcher.disconnect(user_id, session_id)
