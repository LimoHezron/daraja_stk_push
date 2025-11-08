import requests
import base64
from datetime import datetime
from api.auth_token import get_token



access_token = get_token()['access_token']
STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
SHORT_CODE = "174379"
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M%S')
phone_num = "254701859820"
def generate_password():
    password = f'{SHORT_CODE}{PASS_KEY}{TIMESTAMP}'
    encodedPassword = base64.b64encode(password.encode()).decode() #encoding password
    return encodedPassword
def stk_push():
    try:

        print('access token: ', access_token)
        headers={
            "content-Type":"application/json", 
            "Authorization":f'Bearer {access_token}'
        }
        encodedPassword = generate_password()
        pay_info = {    
   "BusinessShortCode": SHORT_CODE,    
   "Password": encodedPassword,    
   "Timestamp":TIMESTAMP,    
   "TransactionType": "CustomerPayBillOnline",    
   "Amount": "30000",    
   "PartyA":phone_num,      
   "PartyB":"174379",    
   "PhoneNumber":phone_num,    
   "CallBackURL": "https://mydomain.com/pat",    
   "AccountReference":"Test",    
   "TransactionDesc":"Limo"
}
        response = requests.post(url=STK_URL,headers=headers,json=pay_info)
        return response.json()
    except Exception as error:
        return {"error": str(error)}
