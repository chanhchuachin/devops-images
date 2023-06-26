from pydantic import BaseModel


class TaskOut(BaseModel):
    task_id: str
    status: str
