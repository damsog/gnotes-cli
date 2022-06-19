from core.API import APIServerEndpoints
from libs.authenticator import Authenticator
from libs.logger import Logger
from getpass import getpass
from rich import print
from libs.printer import print_lists, print_objects
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
            print("[bold magenta]Login to the platform...")
            user = input("username: ")
            password = getpass("password: ")
            try:
                result = self.authenticator.authenticate(user, password)
                if result['result'] == 'success':
                    break
                elif result['result'] == 'failed':
                    print(f'[bold magenta]Login Failed : {result["message"]}')

            except Exception as e:
                print(f'[bold red][X] [magenta]{e}')
            
    def create(self, list, description=None):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not list: 
            print(f'[bold red][X] [magenta]Must specify the list name')
            return
        
        # Preparing the request
        url = self.endpoints.api_list_create
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }        
        payload = json.dumps({ 'name':list,'description': description})

        request_result = requests.request("POST", url=url, headers=headers, data=payload)

        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.create(list, description)
        else:
            # Handlng the request
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                print("[bold magenta] LIST CREATED")
                print_lists([request_result['data']['newList']])
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')

    def modify(self, list, description=None):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not list: 
            print(f'[bold red][X] [magenta]Must specify the list name')
            return
        
        # Preparing the request
        url = self.endpoints.api_list_updateByName.replace(':name', list)
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }        
        payload = json.dumps({ 'name':list,'description': description})

        request_result = requests.request("PUT", url=url, headers=headers, data=payload)

        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.modify(list, description)
        else:
            # Handlng the request
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                print("[bold magenta] OBJECT CREATED")
                print_lists([request_result['data']])
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')

    def delete(self, list):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not list: 
            print(f'[bold red][X] [magenta]Must specify the list name')
            return
        
        # Preparing the request
        url = self.endpoints.api_list_deleteByName.replace(':name', list)
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }        

        request_result = requests.request("DELETE", url=url, headers=headers)
        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.delete(list)
        else:
            # Handlng the request
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                print("[bold magenta] LIST DELETED")
                print(f'[bold magenta]      {request_result["data"]}')
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')

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
                print(f'[bold red][X] [magenta]Must specify the {arg}')
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
                print("[bold magenta] OBJECT ADDED")
                print_objects([request_result['data']])
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')
            
    def update(self):
        pass

    def remove(self, title, list):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not title: 
            print(f'[bold red][X] [magenta]Must specify the name')
            return
        
        if not list: 
            print(f'[bold red][X] [magenta]Must specify the list')
            return
        
        # Preparing the request
        url = self.endpoints.api_object_deleteByName.replace(':objectName',title).replace(':listName', list)
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }        

    
        request_result = requests.request("DELETE", url=url, headers=headers)
        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.remove(title, list)
        else:
            # Handlng the request
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                print("[bold magenta] OBJECT DELETED")
                print_lists(request_result['data'])
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')

    def get(self, list, name=None, filter=None):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        if not list: 
            print(f'[bold red][X] [magenta]Must specify the list')
            return

        if(list=="lists" and not name):
            if(filter): print(f'[bold red][X] [magenta] Filters dont apply to the set of lists themselves. ignoring option')
            
            url = self.endpoints.api_list_getByUserId.replace(':id', self.authenticator.session['user_id'])

            headers = {'content-type': 'application/json',
                       'Authorization': self.authenticator.session['token'] }

            request_result = requests.request("GET", url=url, headers=headers)
            if request_result.text == "Invalid Token":
                self.authenticator.clean_session()
                self.get(list, name, filter)
            else:
                data = json.loads(request_result.text)
                print("[bold magenta] USER LISTS")
                print_lists(data["data"])

        if(list!="lists"):
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
                print(f'[bold magenta] {list.upper()}')
                print_objects(data["data"])
    
    def logout(self):
        self.authenticator.clean_session()