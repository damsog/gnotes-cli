from core.API import APIServerEndpoints
from libs.authenticator import Authenticator
from libs.logger import Logger
from getpass import getpass
import configparser
import requests
import json

class RequestHandler:
    def __init__(self, level="INFO") -> None:
        if level=="DEBUG":
            self.logger = Logger("DEBUG", COLORED=True)
        else:
            self.logger = Logger("INFO", COLORED=True)

        # Configuration
        self.config = configparser.ConfigParser()
        self.config.read('config/config.init')

        # API
        self.server_url = self.config['DEFAULT']['SERVER']
        self.server_port = self.config['DEFAULT']['PORT']
        self.endpoints = APIServerEndpoints(self.server_url, self.server_port)

        self.authenticator = Authenticator(self.endpoints.api_login)

        # List
        self.list_active = False
        self.current_list = None
    
    def login(self):
        tries_remaining = 3
        while(tries_remaining > 0):
            tries_remaining -= 1
            self.logger.info("Login to the platform...")
            user = input("username: ")
            password = getpass("password: ")
            try:
                result = self.authenticator.authenticate(user, password)
                if result['result'] == 'success':
                    break
                elif result['result'] == 'failed':
                    self.logger.info(f'Login Failed : {result["message"]}')

            except Exception as e:
                self.logger.error(e)
            
    def create(self, name, description=None):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not name: 
            self.logger.error(f'Must specify the list name')
            return
        
        # Preparing the request
        url = self.endpoints.api_list_create
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }        
        payload = json.dumps({ 'name':name,'description': description})

        request_result = requests.request("POST", url=url, headers=headers, data=payload)


        # Handlng the response
        request_result = json.loads(request_result.text)

        if request_result['result']=="success":
            self.logger.info("   List Created:")
            self.logger.info(f'      {request_result["data"]["newList"]["name"]} {request_result["data"]["newList"]["description"]}')
        else:
            self.logger.error(f'   {request_result["message"]}')

    def modify(self, name, description=None):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not name: 
            self.logger.error(f'Must specify the list name')
            return
        
        # Preparing the request
        url = self.endpoints.api_list_updateByName.replace(':name', name)
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }        
        payload = json.dumps({ 'name':name,'description': description})

        request_result = requests.request("PUT", url=url, headers=headers, data=payload)

        # Handlng the request
        request_result = json.loads(request_result.text)

        if request_result['result']=="success":
            self.logger.info("   List Updated:")
            self.logger.info(f'      {request_result["data"]["name"]} {request_result["data"]["description"]}')
        else:
            self.logger.error(f'   {request_result["message"]}')

    def delete(self, name):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not name: 
            self.logger.error(f'Must specify the list name')
            return
        
        # Preparing the request
        url = self.endpoints.api_list_deleteByName.replace(':name', name)
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }        

        request_result = requests.request("DELETE", url=url, headers=headers)

        # Handlng the request
        request_result = json.loads(request_result.text)

        if request_result['result']=="success":
            self.logger.info("   List Deleted:")
            self.logger.info(f'      {request_result["data"]}')
        else:
            self.logger.error(f'   {request_result["message"]}')

    def set(self):
        pass

    def unset(self):
        pass
    
    def add(self, **kwargs):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return

        payload = {}
        for arg,val in kwargs.items():
            if( arg=='title' and val==None) or (arg=='listName' and val==None): 
                self.logger.error(f'Must specify the {arg}')
                return
            
            payload[arg]= val if val else ""
        
        # Preparing the request
        url = self.endpoints.api_object_createByListName
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }

        payload = json.dumps(payload)

        request_result = requests.request("POST", url=url, headers=headers, data=payload)

        # Handlng the response
        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.add(kwargs)
        else:
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                self.logger.info("   Object Added:")
                self.logger.info(f'      {request_result["data"]["title"]} {request_result["data"]["description"]}')
            else:
                self.logger.error(f'   {request_result["message"]}')
            
            
        

    def update(self):
        pass

    def remove(self):
        pass

    def get(self, list, name=None, filter=None):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not list: 
            self.logger.error(f'Must specify the list')
            return

        if(list=="lists" and not name):
            if(filter): self.logger.warning("Filters dont apply to the set of lists themselves. ignoring option")
            
            url = self.endpoints.api_list_getByUserId.replace(':id', self.authenticator.session['user_id'])

            headers = {'content-type': 'application/json',
                       'Authorization': self.authenticator.session['token'] }

            request_result = requests.request("GET", url=url, headers=headers)
            if request_result.text == "Invalid Token":
                self.authenticator.clean_session()
                self.get(list, name, filter)
            else:
                data = json.loads(request_result.text)
                self.logger.info("   User Lists:")
                for object in data['data']:
                    self.logger.info(f'      {object["name"]} {object["description"]}')

        # Preparing the request     
        url = self.endpoints.api_object_getByListName.replace(':name', list)

        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }

        request_result = requests.request("GET", url=url, headers=headers)
        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.get(list, name, filter)
        else:
            data = json.loads(request_result.text)
            self.logger.info("   User Lists:")
            for object in data['data']:
                self.logger.info(f'      {object["title"]} {object["description"]}')
    
    def logout(self):
        self.authenticator.clean_session()