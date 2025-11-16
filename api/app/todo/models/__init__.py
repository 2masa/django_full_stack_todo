

from enum import StrEnum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class TodoStatus(StrEnum):
    OPEN = "Open"
    PENDING = "Pending"
    INPROGRESS = "InProgress"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    

class TodoPriorityStatus(StrEnum):
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"



class TodoCreate(BaseModel):
    title: str
    description:str
    priority : TodoPriorityStatus
    status:TodoStatus

class TodoUpdate(BaseModel):
    id:UUID
    title: Optional[str] = None
    description:Optional[str] = None
    priority : Optional[TodoPriorityStatus] = None
    status: Optional[TodoStatus] = None


