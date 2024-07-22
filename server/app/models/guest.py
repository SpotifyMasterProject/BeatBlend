from pydantic import BaseModel


class Guest(BaseModel):
    username: str
