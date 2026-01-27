"""
WebSocket for real-time manuscript autosave
"""

from typing import Dict
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from api.manuscripts import autosave_manuscript
from schemas.manuscript import ManuscriptUpdate
import json

router = APIRouter()

# 활성 연결 관리
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, scene_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[scene_id] = websocket
    
    def disconnect(self, scene_id: str):
        if scene_id in self.active_connections:
            del self.active_connections[scene_id]
    
    async def send_message(self, scene_id: str, message: dict):
        if scene_id in self.active_connections:
            await self.active_connections[scene_id].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/scene/{scene_id}")
async def websocket_autosave(
    websocket: WebSocket,
    scene_id: str
):
    """
    WebSocket 자동저장 연결
    
    클라이언트가 보내는 메시지 형식:
    {
        "action": "save",
        "content": "원고 내용..."
    }
    """
    await manager.connect(scene_id, websocket)
    
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "save":
                content = message.get("content", "")
                
                # DB 세션 생성 (WebSocket은 Depends 사용 불가)
                from core.database import SessionLocal
                db = SessionLocal()
                
                try:
                    # 자동저장 실행
                    scene_uuid = UUID(scene_id)
                    manuscript_data = ManuscriptUpdate(content=content)
                    result = await autosave_manuscript(scene_uuid, manuscript_data, db)
                    
                    # 저장 성공 응답
                    await manager.send_message(scene_id, {
                        "status": "saved",
                        "word_count": result.word_count,
                        "saved_at": result.auto_saved_at.isoformat() if result.auto_saved_at else None
                    })
                    
                except Exception as e:
                    # 저장 실패 응답
                    await manager.send_message(scene_id, {
                        "status": "error",
                        "message": str(e)
                    })
                
                finally:
                    db.close()
    
    except WebSocketDisconnect:
        manager.disconnect(scene_id)
    
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(scene_id)
