import requests
import base64

url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
CONSUMER_KEY ="uRIcNztgyTelTqhPoqDqewRNTBWyGhgUmpUsAbpUh8eRPM67"
CONSUMER_SECRET ="lBjWGGKyV8wnSwwlhRYg90IiiObuiRc0tuM2hjEbd6RbNo006nHuKgGgO6Q3EDZW"

def get_token():
    try: 
        credentials = f'{CONSUMER_KEY}:{CONSUMER_SECRET}'
        encodedCredentials = base64.b64encode(credentials.encode()).decode() #encoding base64
        # return encodedCredentials
        headers = {"Authorization": f'Basic {encodedCredentials}'}
        response = requests.get(url,headers=headers)
        return response.json()

    except Exception as e:
        return{'error': str(e)}