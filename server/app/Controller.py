from fastapi import FastAPI, HTTPException
from app.models.user import User
from app.models.session import Session

app = FastAPI()

# TODO: Remove this when we have a DB setup
users = {
 "123": User(user_id="123"),
 "234": User(user_id="234")
}

sessions = {
 "S_1": Session(session_id="S_1", host=users["123"], members=[users["123"]]),
 "S_2": Session(session_id="S_2", host=users["234"], members=[users["234"]])
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

@app.get("/sessions")
def get_sessions() -> dict[str, Session]:
    # TODO: Restrict this API to admin users.
    return sessions

@app.post("/session/store")
def save_session(session: Session) -> Session:
    sessions[session.session_id] = session
    return session

@app.delete("/session/{session_id}")
def delete_session(session_id: str) -> bool:
    del sessions[session_id]

    return True