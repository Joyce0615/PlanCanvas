from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..core.orchestrator import Orchestrator

router = APIRouter()

class DesignRequest(BaseModel):
    prompt: str

@router.post("/")
def create_design(req: DesignRequest):
    """
    POST /design
    Body: { "prompt": "Design a recommendation system" }
    """
    orchestrator = Orchestrator()
    try:
        result = orchestrator.run_design_session(req.prompt)
        return {
            "message": "Design session complete",
            "diagram_data": result["diagram"],
            "agent_log": result["log"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
