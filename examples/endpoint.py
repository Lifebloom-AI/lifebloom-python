# Description: This file contains example FastAPI endpoints for the Lifebloom SDK.

import fastapi
from lifebloom import thread_completion, initialize_thread_state
from pydantic import BaseModel

app = fastapi.FastAPI()

class ThreadCompletionRequest(BaseModel):
    thread_state: dict
    actions_response: list
    
class InitializeThreadStateRequest(BaseModel):
    thread_input: dict
    workflow_name: str
    mode: str
    persona_object: dict


@app.post("/thread_completion")
def thread_completion(request):
    return thread_completion(request.thread_state, request.actions_response)


@app.post("/initialize_thread_state")
def initialize_thread_state(request):
    return initialize_thread_state(request.thread_input, request.workflow_name, request.mode, request.persona_object)