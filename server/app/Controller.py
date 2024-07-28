from fastapi import FastAPI, HTTPException
from app.models.user import User

app = FastAPI()

# TODO: Remove this when we have a DB setup
users = {
 "123": User(user_id="123")
}

@app.get("/")
def read_root():
    return {"Hello": "World!"}


@app.get("/users/{user_id}")
def get_user(user_id: str) -> User:
    # TODO: Implement the GET user endpoint using the DB.
    user = users.get(user_id, None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
