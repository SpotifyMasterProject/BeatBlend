from pydantic import BaseModel

class User(BaseModel):
    """ 
    Model that specifies the data we store about 
    a user.

    TODO: Add fields to the user model.
    """
    user_id: str
