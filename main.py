# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from api.auth_token import get_token
# # from api.stk_prompter import stk_push
# import requests
# import base64
# from datetime import datetime



# app = FastAPI()





# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# class formData(BaseModel):
#     number:str
#     amount:str


# # from api.auth_token import get_token




# access_token = get_token()['access_token']
# STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
# SHORT_CODE = "174379"
# PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
# TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M%S')
# def generate_password():
#     password = f'{SHORT_CODE}{PASS_KEY}{TIMESTAMP}'
#     encodedPassword = base64.b64encode(password.encode()).decode() #encoding password
#     return encodedPassword
# def stk_push(phone_num,amount):
#     try:

#         print('access token: ', access_token)
#         headers={
#             "content-Type":"application/json", 
#             "Authorization":f'Bearer {access_token}'
#         }
#         encodedPassword = generate_password()
#         pay_info = {    
#    "BusinessShortCode": SHORT_CODE,    
#    "Password": encodedPassword,    
#    "Timestamp":TIMESTAMP,    
#    "TransactionType": "CustomerPayBillOnline",    
#    "Amount": amount, #amount hardcoded   
#    "PartyA":phone_num,      
#    "PartyB":"174379",    
#    "PhoneNumber":phone_num,    
#    "CallBackURL": "https://mydomain.com/pat",    
#    "AccountReference":"Test",    
#    "TransactionDesc":"Limo"
# }
#         response = requests.post(url=STK_URL,headers=headers,json=pay_info)
#         return response.json()
#     except Exception as error:
#         return {"error": str(error)}

# @app.get("/get_token")
# def getacces_token():
#     access_token = get_token()
#     return access_token   
    
# @app.post("/stk_push")
# def get_push(data: formData):
#     return stk_push(data.number,data.amount)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, base64
from datetime import datetime
from api.auth_token import get_token

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for frontend input
class FormData(BaseModel):
    number: str
    amount: str

# M-PESA configuration
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
SHORT_CODE = "174379"
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

# Generate encoded password
def generate_password(timestamp):
    raw = f'{SHORT_CODE}{PASS_KEY}{timestamp}'
    return base64.b64encode(raw.encode()).decode()

# Function to make STK push
def make_stk_push(phone_num, amount):
    access_token = get_token()['access_token']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = generate_password(timestamp)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    pay_info = {
        "BusinessShortCode": SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_num,
        "PartyB": SHORT_CODE,
        "PhoneNumber": phone_num,
        "CallBackURL": "https://your-ngrok-url.ngrok.io/callback",
        "AccountReference": "Limo",
        "TransactionDesc": "Limo"
    }

    response = requests.post(url=STK_URL, headers=headers, json=pay_info)
    return response.json()

# Routes
@app.get("/get_token")
def get_access_token():
    return get_token()

@app.post("/stk_push")
def stk_push_route(data: FormData):
    return make_stk_push(data.number, data.amount)
