from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str

class TodoSchema(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True