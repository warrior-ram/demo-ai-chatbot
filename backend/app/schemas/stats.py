from pydantic import BaseModel

class DashboardStatsResponse(BaseModel):
    total_sessions: int
    total_leads: int
    active_bots: int
    total_documents: int
