from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
import json

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from .websocket import manager

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session

# User Endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Poll Endpoints
@app.post("/polls/", response_model=schemas.Poll)
def create_poll(poll: schemas.PollCreate, creator_id: int, db: Session = Depends(get_db)):
    # In a real app, creator_id would come from authentication
    return crud.create_poll(db=db, poll=poll, creator_id=creator_id)

@app.get("/polls/{poll_id}", response_model=schemas.Poll)
def read_poll(poll_id: int, db: Session = Depends(get_db)):
    db_poll = crud.get_poll_with_vote_counts(db, poll_id=poll_id)
    if db_poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return db_poll

# Vote Endpoints
@app.post("/polls/{poll_id}/vote", response_model=schemas.Vote)
async def vote_on_poll(poll_id: int, vote: schemas.VoteCreate, user_id: int, db: Session = Depends(get_db)):
    # In a real app, user_id would come from authentication
    db_vote = crud.create_user_vote(db=db, vote=vote, user_id=user_id)
    if db_vote is None:
        raise HTTPException(status_code=404, detail="Poll option not found or other error")

    # After a vote, broadcast updated results to WebSocket clients for this poll
    updated_poll = crud.get_poll_with_vote_counts(db, poll_id=poll_id)
    if updated_poll:
        await manager.broadcast(json.dumps(schemas.Poll.model_validate(updated_poll).model_dump()), poll_id)

    return db_vote

# WebSocket Endpoint
@app.websocket("/ws/poll/{poll_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket, poll_id)
    try:
        while True:
            # Keep the connection alive, or handle incoming messages if needed
            # For this app, we only broadcast from the server, so we can just await messages
            # or implement a ping/pong mechanism if client-to-server communication is expected.
            data = await websocket.receive_text()
            # Optionally handle messages from client, e.g., client requests specific data
            # For now, we just keep the connection open.
            print(f"Message from client for poll {poll_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, poll_id)
        print(f"Client for poll {poll_id} disconnected")
