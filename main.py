import redis
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Initialize Redis client
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

class UserData(BaseModel):
    username: str
    server_url: str

@app.post("/register_user")
def register_user(data: UserData):
    try:
        # Store the server URL for the user in Redis
        redis_client.set(data.username, data.server_url)
        return {"status": "User registered"}
    except Exception as e:
        return {"error": f"Failed to register user: {str(e)}"}

@app.get("/get_server/{username}")
def get_server(username: str):
    try:
        # Get the server URL for the user from Redis
        server_url = redis_client.get(username)
        if server_url:
            return {"server_url": server_url}
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

