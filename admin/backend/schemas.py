from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClientBase(BaseModel):
    telegram_id: int
    username: str
    full_name: str

class ClientRead(ClientBase):
    id: int
    created_at: datetime  # <- поменяли на datetime

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    client_id: int
    project_type: str
    duration_raw: str
    duration_final: str
    services: List[str]
    deadline: str
    budget: str
    source_links: Optional[str]
    style_examples: Optional[str]
    additional_notes: Optional[str]
    status: Optional[str]

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime  # <- поменяли на datetime
    updated_at: Optional[datetime]  # <- поменяли на datetime

    class Config:
        orm_mode = True
