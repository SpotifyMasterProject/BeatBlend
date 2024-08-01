from pydantic import BaseModel
from .user import User

class Session(BaseModel):
    """ 
    Model that specifies the data we store about 
    a session.
    """
    session_id: str
    host: User
    members: list[User]