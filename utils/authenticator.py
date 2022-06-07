import requests
import json

class Authenticator:
    def __init__(self, username, password, url)-> None:
        self.url = url
        credentials = { 'username': username, 'password': password }

        authentication = requests.post(self.url, credentials)

        self.token = json.loads(authentication.text).data.token
    
    def get_token(self):
        return self.token