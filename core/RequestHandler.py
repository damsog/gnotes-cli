import shutil
from libs.printer import print_lists, print_objects, print_details
from core.API import APIServerEndpoints
from libs.authenticator import Authenticator
from libs.logger import Logger
from os.path import exists
from rich.prompt import Prompt
from rich import print
import configparser
import requests
import json

class RequestHandler:
    def __init__(self, main_path, level="INFO") -> None:
        if level=="DEBUG":
            self.logger = Logger("DEBUG", COLORED=True)
        else:
            self.logger = Logger("INFO", COLORED=True)

        # Configuration
        self.main_path=main_path
        if not exists(f'{self.main_path}/config/config.init'): shutil.copyfile(f'{self.main_path}/config/config.init.BASE',f'{self.main_path}/config/config.init')
        self.config = configparser.ConfigParser()
        self.config.read(f'{self.main_path}/config/config.init')

        # API
        self.server_url = self.config['DEFAULT']['SERVER']
        self.server_port = self.config['DEFAULT']['PORT']
        self.endpoints = APIServerEndpoints(self.server_url, self.server_port)

        self.authenticator = Authenticator(self.endpoints.api_login, self.main_path)

        # List
        self.list_active = False
        self.current_list = None
    
    def login(self):
        tries_remaining = 3
        while(tries_remaining > 0):
            tries_remaining -= 1
            print("[bold magenta]Login to the platform...")
            user = Prompt.ask("[bold magenta]username: ")
            password = Prompt.ask("[bold magenta]password: ", password=True)
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

    def set(self, list):
        # TODO: Request to check if list exist
        if(not list): return
        self.config['SESSION']['ACTIVE_LIST']=list
        with open(f'{self.main_path}/config/config.init', 'w') as configfile:
            self.config.write(configfile)
        print(f'[bold magenta]LIST {list.upper()} SET')

    def unset(self):
        self.config['SESSION']['ACTIVE_LIST']='None'
        with open(f'{self.main_path}/config/config.init', 'w') as configfile:
            self.config.write(configfile)
        print(f'[bold magenta]LIST UNSET')
    
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
  
    def update(self, **kwargs ):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        payload = {}
        for arg,val in kwargs.items():
            if( arg=='title' and val==None) or (arg=='listName' and val==None): 
                print(f'[bold red][X] [magenta]Must specify the {arg}')
                return
            
            if((arg!='title' or arg!='listName') and val): payload[arg]= val
        
        # Preparing the request
        url = self.endpoints.api_object_updateByName.replace(':objectName', kwargs['title']).replace(':listName', kwargs['listName'])
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }

        payload = json.dumps(payload)

        request_result = requests.request("PUT", url=url, headers=headers, data=payload)

        # Handlng the response
        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.update(kwargs)
        else:
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                print("[bold magenta] OBJECT UPDATED")
                print_objects([request_result['data']])
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')
        
    def update_add(self, **kwargs ):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        payload = {}
        for arg,val in kwargs.items():
            if( arg=='title' and val==None) or (arg=='listName' and val==None): 
                print(f'[bold red][X] [magenta]Must specify the {arg}')
                return
            
            if((arg!='title' or arg!='listName') and val): payload[arg]= val
        
        # Preparing the request
        url = self.endpoints.api_object_updateOptionsByName.replace(':objectName', kwargs['title']).replace(':listName', kwargs['listName'])
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }

        payload = json.dumps(payload)

        request_result = requests.request("PUT", url=url, headers=headers, data=payload)

        # Handlng the response
        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.update_add(kwargs)
        else:
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                print("[bold magenta] OBJECT UPDATED")
                print_objects([request_result['data']])
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')

    def update_remove(self, **kwargs ):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return
    
        payload = {}
        for arg,val in kwargs.items():
            if( arg=='title' and val==None) or (arg=='listName' and val==None): 
                print(f'[bold red][X] [magenta]Must specify the {arg}')
                return
            
            if((arg!='title' or arg!='listName') and val): payload[arg]= val
        
        # Preparing the request
        url = self.endpoints.api_object_removeOptionsByName.replace(':objectName', kwargs['title']).replace(':listName', kwargs['listName'])
        headers = {'content-type': 'application/json',
                    'Authorization': self.authenticator.session['token'] }

        payload = json.dumps(payload)

        request_result = requests.request("DELETE", url=url, headers=headers, data=payload)

        # Handlng the response
        if request_result.text == "Invalid Token":
            self.authenticator.clean_session()
            self.update_remove(kwargs)
        else:
            if(not request_result.text): return
            request_result = json.loads(request_result.text)
            if request_result['result']=="success":
                print("[bold magenta] OBJECT UPDATED")
                print_objects([request_result['data']])
            else:
                print(f'[bold red][X] [magenta]{request_result["message"]}')

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
                print(f'[bold magenta]      {request_result["data"]}')
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
                request_result = json.loads(request_result.text)
                if request_result['result']=="success":
                    print("[bold magenta] USER LISTS")
                    print_lists(request_result["data"])
                else:
                    print(f'[bold red][X] [magenta]{request_result["message"]}')

        if(list!="lists" and not name and not filter):
            # Preparing the request     
            url = self.endpoints.api_object_getByListName.replace(':name', list)

            headers = {'content-type': 'application/json',
                        'Authorization': self.authenticator.session['token'] }

            request_result = requests.request("GET", url=url, headers=headers)
            if request_result.text == "Invalid Token":
                self.authenticator.clean_session()
                self.get(list, name, filter)
            else:
                request_result = json.loads(request_result.text)
                if request_result['result']=="success":
                    print(f'[bold magenta] {list.upper()}')
                    print_objects(request_result["data"])
                else:
                    print(f'[bold red][X] [magenta]{request_result["message"]}')
        
        if(list!="lists" and not name and filter):
            # Preparing the request     
            url = self.endpoints.api_object_getByFilters.replace(':listName', list)

            headers = {'content-type': 'application/json',
                        'Authorization': self.authenticator.session['token'] }

            payload = json.dumps({ 'filters':filter })

            request_result = requests.request("POST", url=url, headers=headers, data=payload)
            if request_result.text == "Invalid Token":
                self.authenticator.clean_session()
                self.get(list, name, filter)
            else:
                request_result = json.loads(request_result.text)
                if request_result['result']=="success":
                    print(f'[bold magenta] {list.upper()}')
                    print_objects(request_result["data"])
                else:
                    print(f'[bold red][X] [magenta]{request_result["message"]}')
        
        if(name):
            # Preparing the request     
            url = self.endpoints.api_object_getByName.replace(':objectName',name).replace(':listName', list)

            headers = {'content-type': 'application/json',
                        'Authorization': self.authenticator.session['token'] }

            request_result = requests.request("GET", url=url, headers=headers)
            if request_result.text == "Invalid Token":
                self.authenticator.clean_session()
                self.get(list, name, filter)
            else:
                request_result = json.loads(request_result.text)
                if request_result['result']=="success":
                    print(f'[bold magenta] {list.upper()}')
                    print_objects([request_result["data"]])
                    print_details(request_result["data"]["information"])
                else:
                    print(f'[bold red][X] [magenta]{request_result["message"]}')

    
    def logout(self):
        self.authenticator.clean_session()