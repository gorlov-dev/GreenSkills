from typing import Dict, Optional
from fastapi import WebSocket
from collections import defaultdict

from starlette.websockets import WebSocketState


class EventDispatcher:
    """Менеджер WebSocket-соединений"""

    def __init__(self):
        # Список соединений авторизованных пользователей (user_id -> {session_id: WebSocket})
        self.auth_connections: Dict[int, Dict[str, WebSocket]] = defaultdict(dict)
        # Список соединений неавторизованных пользователей (session_id -> WebSocket)
        self.guest_connections: Dict[str, WebSocket] = {}

    async def connect(
        self, user_id: Optional[int], session_id: str, websocket: WebSocket
    ):
        """Подключение клиента"""
        if user_id is None:
            self.guest_connections[session_id] = websocket
        else:
            self.auth_connections[user_id][session_id] = websocket

    async def authorize_connection(self, user_id: int, session_id: str):
        self.auth_connections[user_id][session_id] = self.guest_connections[session_id]
        del self.guest_connections[session_id]

    async def disconnect(self, user_id: Optional[int], session_id: str):
        """Отключение клиента"""
        if user_id is None:
            if session_id in self.guest_connections:
                ws = self.guest_connections[session_id]
                if ws.client_state == WebSocketState.CONNECTED:
                    await self.guest_connections[session_id].close()
                    del self.guest_connections[session_id]
        else:
            if (
                user_id in self.auth_connections
                and session_id in self.auth_connections[user_id]
            ):
                ws = self.auth_connections[user_id][session_id]
                if ws.client_state == WebSocketState.CONNECTED:
                    await self.auth_connections[user_id][session_id].close()
                    del self.auth_connections[user_id][session_id]

                if not self.auth_connections[user_id]:
                    del self.auth_connections[user_id]

    async def send(
        self, user_id: Optional[int], session_id: str, event: str, data: dict
    ):
        """Отправка данных в нужное соединение"""
        if user_id is None:
            if session_id in self.guest_connections:
                ws = self.guest_connections[session_id]
                if ws.client_state == WebSocketState.CONNECTED:
                    await ws.send_json({"event": event, "data": data})
        else:
            if (
                user_id in self.auth_connections
                and session_id in self.auth_connections[user_id]
            ):
                ws = self.auth_connections[user_id][session_id]
                if ws.client_state == WebSocketState.CONNECTED:
                    await self.auth_connections[user_id][session_id].send_json(
                        {"event": event, "data": data}
                    )

    async def send_all(self, user_id: int, event: str, data: dict):
        """Отправка данных во все вкладки авторизованного пользователя"""
        if user_id in self.auth_connections:
            for ws in self.auth_connections[user_id].values():
                await ws.send_json({"event": event, "data": data})


event_dispatcher = EventDispatcher()
