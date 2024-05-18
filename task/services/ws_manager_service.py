from fastapi import WebSocket, HTTPException
from uuid import UUID
from typing import Dict
from task.schemas.task_schemas import TaskProfile
from task.services.auth_service import get_user
import json

WS_DIR: Dict[UUID, WebSocket] = {}


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID:WebSocket] = WS_DIR

    async def connect(self, user_uid: UUID, websocket: WebSocket):
        try:
            await get_user(user_uid=user_uid)
            await websocket.accept()
            await websocket.send_json({"message": "ws connected"})
            self.active_connections[user_uid] = websocket
        except HTTPException:
            await websocket.send_json({"detail": "user not found"})
            await websocket.close()

    async def disconnect(self, user_uid: UUID):
        if self.active_connections.get(user_uid):
            websocket: WebSocket = self.active_connections.pop(user_uid)
            await websocket.close()

    async def send_personal_message(self, task: TaskProfile):
        if self.active_connections.get(task.user_uid):
            websocket: WebSocket = self.active_connections.get(task.user_uid)
            task_profile = json.loads(json.dumps(task.model_dump(), default=str))
            await websocket.send_json(task_profile)


manager = ConnectionManager()
