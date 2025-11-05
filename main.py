from fastapi import FastAPI
from api.auth_token import get_token
from api.stk_prompter import stk_push

app = FastAPI()
@app.get("/get_token")
def getacces_token():
    access_token = get_token()
    return access_token

@app.post("/stk_push")
def get_push():
    stk_prompt = stk_push()
    return stk_prompt


