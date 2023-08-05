from rest_framework import authentication
from .models import TokenUser
import os, requests, jwt

VERIFY_URL = os.environ['VERIFY_URL']

HEADERS = {
    'Content-Type': 'application/json', 
}

def verify(token):
    response = requests.post(VERIFY_URL, headers=HEADERS, json={"token": token})
    return {
        'status_code': response.status_code,
        'data': response.json()
    }

class MyJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]

        response = verify(token)
        if response['status_code'] == 200:
            decode_token = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
            user = TokenUser()
            user.from_json(decode_token['user'])
            return user, None
            
        return None, None
