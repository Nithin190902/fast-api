from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class TodoInDB(TodoBase):
    id: int

    class Config:
        orm_mode = True