import os
from os.path import exists
import requests
import pickle
import json

class Authenticator:
    def __init__(self, url, username=None, password=None)-> None:
        self.url = url
        self.session = {'user_id':None,'token':None}
        self.is_authenticated = False

        if(username is not None and password is not None):
            credentials = { 'username': username, 'password': password }
            authentication = requests.post(self.url, credentials)

            result = json.loads(authentication.text)
            self.session['token'] = result['data']['token']
            self.session['user_id'] = result['data']['_id']
            self.is_authenticated = True
            self.save_session()
        else:
            self.session['token'] = None
            self.session['user_id'] = None
            self.is_authenticated = False
            self.read_session()
    
    def read_session(self):
        session_exists = exists('session.pickle')

        if session_exists:
            try:
                with open("session.pickle", "rb") as session_to_save:
                    self.session = pickle.load(session_to_save)
                    self.is_authenticated = True

            except Exception as e:
                self.session = {'user_id':None,'token':None}
                self.is_authenticated = False

    def save_session(self):
        with open("session.pickle", "wb") as session_to_save:
            pickle.dump(self.session, session_to_save)
    
    def clean_session(self):
        self.session = {'user_id':None,'token':None}
        self.is_authenticated = False
        try:
            os.remove('session.pickle')
        except Exception as e:
            pass
        
    def authenticate(self, username, password):
        credentials = { 'username': username, 'password': password }
        authentication = requests.post(self.url, credentials)

        result = json.loads(authentication.text)

        if result['result']=='success':
            self.session['token'] = result['data']['token']
            self.session['user_id'] = result['data']['_id']
            self.is_authenticated = True
            self.save_session()

        return result