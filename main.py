import redis
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Initialize Redis client
redis_client = redis.StrictRedis(host="redis-stack", port=6379, db=0, decode_responses=True)


class UserData(BaseModel):
    username: str
    queue_name: str

@app.post("/register_user")
def register_user(data: UserData):
    try:
        # Store the server URL for the user in Redis
        redis_client.set(data.username, data.queue_name)
        return {"status": "User registered"}
    except Exception as e:
        return {"error": f"Failed to register user: {str(e)}"}

@app.get("/get_server/{username}")
def get_server(username: str):
    try:
        # Get the server URL for the user from Redis
        queue_name = redis_client.get(username)
        if queue_name:
            return {"queue_name": queue_name}
        else:
            return {"error": f"User {username} not found"}
    except Exception as e:
        return {"error": f"Failed to retrieve server URL: {str(e)}"}

@app.post("/remove_user")
def remove_user(data: UserData):
    try:
        # Remove the user from Redis
        redis_client.delete(data.username)
        return {"status": "User removed"}
    except Exception as e:
        return {"error": f"Failed to remove user: {str(e)}"}

