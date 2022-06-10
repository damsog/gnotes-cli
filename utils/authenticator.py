import requests
import json

class Authenticator:
    def __init__(self, url, username=None, password=None)-> None:
        self.url = url

        if(username is not None and password is not None):
            credentials = { 'username': username, 'password': password }
            authentication = requests.post(self.url, credentials)

            self.token = json.loads(authentication.text).data.token
            self.is_authenticated = True
        else:
            self.is_authenticated = False
            self.token = None
    
    def authenticate(self, username, password):
        credentials = { 'username': username, 'password': password }
        authentication = requests.post(self.url, credentials)

        self.token = json.loads(authentication.text).data.token
        self.is_authenticated = True

    def get_token(self):
        return self.token