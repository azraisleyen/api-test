from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Demo API", version="1.0")

class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=120)

class User(UserIn):
    id: int

def _seed_db():
    return {
        1: User(id=1, name="Alice", age=30),
        2: User(id=2, name="Bob", age=25),
    }

_DB = _seed_db()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in _DB:
        raise HTTPException(status_code=404, detail="User not found")
    return _DB[user_id]

@app.post("/users", status_code=201)
def create_user(payload: UserIn):
    new_id = max(_DB.keys()) + 1
    u = User(id=new_id, **payload.model_dump())
    _DB[new_id] = u
    return u

@app.put("/users/{user_id}")
def update_user(user_id: int, payload: UserIn):
    if user_id not in _DB:
        raise HTTPException(status_code=404, detail="User not found")
    updated = User(id=user_id, **payload.model_dump())
    _DB[user_id] = updated
    return updated

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in _DB:
        raise HTTPException(status_code=404, detail="User not found")
    del _DB[user_id]
    return

@app.post("/__reset", status_code=204)
def reset_db():
    global _DB
    _DB = _seed_db()
    return


