from fastapi import APIRouter
from datetime import datetime
from typing import Dict

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict:
    """Endpoint de salud del sistema"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
