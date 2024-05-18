from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from task.services.service_utils.auth_utils import verify_access_token
from task.services.ws_manager_service import manager
from fastapi.responses import RedirectResponse
from task.root.api_router import router
import logging
import asyncio


LOGGER = logging.getLogger(__name__)


def intialize() -> FastAPI:
    app = FastAPI()
    app.include_router(router=router)

    return app


app = intialize()


@app.get("/", status_code=307)
def root():
    return RedirectResponse(url="/docs")


@app.websocket("/ws/task/")
async def websocket_endpoint(websocket: WebSocket, access_token: str):
    try:
        token_data = await verify_access_token(token=access_token)

        await manager.connect(websocket=websocket, user_uid=token_data.user_uid)
        try:
            while True:
                await asyncio.sleep(0.5)
                pass
        except WebSocketDisconnect:
            await manager.disconnect(user_uid=token_data.user_uid)
    except Exception:
        await websocket.send_json({"detail": "token invalid or expired"})
        await websocket.close()
