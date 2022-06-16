from utils.authenticator import Authenticator
from utils.logger import Logger
from getpass import getpass
import configparser
import argparse
import requests
import json

class APIServerEndpoints:
    def __init__(self, server_url=None, server_port=None)-> None:

        if (server_url and server_port):
            self.api_base = f'http://{server_url}:{server_port}/api'
        else:
            self.api_base = "/api" 
        
        # Access endpoints
        self.api_base_access = f'{self.api_base}/access'
        self.api_login = f'{self.api_base_access}/login'
        self.api_create = f'{self.api_base_access}/create'

        # User endpoints
        self.api_base_user = f'{self.api_base}/users'
        self.api_user_getAll = f'{self.api_base_user}/getAll'
        self.api_user_getById = f'{self.api_base_user}/getById/:id'
        self.api_user_getByUsername = f'{self.api_base_user}/getByUsername/:username'
        self.api_user_getByEmail = f'{self.api_base_user}/getByEmail/:email'
        self.api_user_update = f'{self.api_base_user}/update/:id'
        self.api_user_delete = f'{self.api_base_user}/delete/:id'

        # List endpoints
        self.api_base_list = f'{self.api_base}/lists'
        self.api_list_create = f'{self.api_base_list}/create'
        self.api_list_getAll = f'{self.api_base_list}/getAll'
        self.api_list_getByUserId = f'{self.api_base_list}/getByUserId/:id'
        self.api_list_get = f'{self.api_base_list}/get/:id'
        self.api_list_getByName = f'{self.api_base_list}/getByName/:name'
        self.api_list_update = f'{self.api_base_list}/update/:id'
        self.api_list_delete = f'{self.api_base_list}/delete/:id'


        # Object endpoints
        self.api_base_object = f'{self.api_base}/objects'
        self.api_object_create = f'{self.api_base_object}/create'
        self.api_object_createByListName = f'{self.api_base_object}/createByListName'
        self.api_object_getAll = f'{self.api_base_object}/getAll'
        self.api_object_getByListId = f'{self.api_base_object}/getByListId/:id'
        self.api_object_getByListName = f'{self.api_base_object}/getByListName/:name'
        self.api_object_getByFilters = f'{self.api_base_object}/getByFilters/:listName'
        self.api_object_get = f'{self.api_base_object}/get/:id'
        self.api_object_getByName = f'{self.api_base_object}/getByName/:objectName/:listName'
        self.api_object_update = f'{self.api_base_object}/update/:id'
        self.api_object_updateByName = f'{self.api_base_object}/updateByName/:objectName/:listName'
        self.api_object_updateOptions = f'{self.api_base_object}/updateOptions/:id'
        self.api_object_updateOptionsByName = f'{self.api_base_object}/updateOptionsByName/:objectName/:listName'
        self.api_object_removeOptions  = f'{self.api_base_object}/removeOptions/:id' 
        self.api_object_removeOptionsByName = f'{self.api_base_object}/removeOptionsByName/:objectName/:listName'
        self.api_object_delete = f'{self.api_base_object}/delete/:id'
        self.api_object_deleteByName = f'{self.api_base_object}/deleteByName/:objectName/:listName'

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


        # Handlng the request
        request_result = json.loads(request_result.text)

        if request_result['result']=="success":
            self.logger.info("   List Created:")
            self.logger.info(f'      {request_result["data"]["newList"]["name"]} {request_result["data"]["newList"]["description"]}')
        else:
            self.logger.error(f'   {request_result["message"]}')

    def modify(self, name, description=None):
        pass

    def delete(self):
        pass

    def set(self):
        pass

    def unset(self):
        pass
    
    def add(self, name, list, description=None, filter=None, attachments=None, information=None):
        if not self.authenticator.is_authenticated: 
            self.login()
            if not self.authenticator.is_authenticated: return

        if not name: 
            self.logger.error(f'Must specify the object name')
            return

        if not list: 
            self.logger.error(f'Must specify the list')
            return
        

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
    
    def logout(self):
        self.authenticator.clean_session()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=[
        "create", 
        "modify",
        "delete",
        "set",
        "unset",
        "add",
        "update",
        "remove",
        "get",
        "logout"], help="S.")
    ap.add_argument("-n", "--name", required=False, help="Element name")
    ap.add_argument("-d", "--description", required=False, help="Element description. This option Substitutes previous description.")
    ap.add_argument("-l", "--list", required=False, help="List name.")
    ap.add_argument("-f", "--filters", required=False, help="Sets filters. This option Substitutes previous filters. \
                                                            Usage: <filter> or <filter>=><value> or <filter>=>[<value>,<value>,..] \
                                                            chain multiple options using '|'  ")
    ap.add_argument("-a", "--attachments", required=False, help="Sets Attachments to object. This option Substitutes previous attachments. \
                                                            Usage: <attachment> or <attachment>=><value> or <attachment>=>[<value>,<value>,..] \
                                                            chain multiple options using '|'  ")
    ap.add_argument("-af", "--add-filters", required=False, help="Add filters. This option Substitutes previous filters. \
                                                            Usage: <filter> or <filter>=><value> or <filter>=>[<value>,<value>,..] \
                                                            chain multiple options using '|'  ")
    ap.add_argument("-aa", "--add-attachments", required=False, help="Add Attachments to object. This option Substitutes previous attachments. \
                                                            Usage: <attachment> or <attachment>=><value> or <attachment>=>[<value>,<value>,..] \
                                                            chain multiple options using '|'  ")
    ap.add_argument("-rf", "--remove-filters", required=False, help="Remove filters. This option Substitutes previous filters. \
                                                            Usage: <filter> or <filter>=><value> or <filter>=>[<value>,<value>,..] \
                                                            chain multiple options using '|'  ")
    ap.add_argument("-ra", "--remove-attachments", required=False, help="Remove Attachments to object. This option Substitutes previous attachments. \
                                                            Usage: <attachment> or <attachment>=><value> or <attachment>=>[<value>,<value>,..] \
                                                            chain multiple options using '|'  ")
    ap.add_argument("-i", "--information", required=False, help="Extra information about the object")
    ap.add_argument("-v", "--verbose", action="store_true", help="Debug level for logger output")
    args = vars(ap.parse_args())

    if args['verbose']:
        logger = Logger("DEBUG", COLORED=True)
    else:
        logger = Logger("INFO", COLORED=True)

    requests_handler = RequestHandler()

    if args["command"] =="create":
        requests_handler.create(args["name"], args["description"])

    if args["command"] =="modify":
        pass

    if args["command"] =="delete":
        pass

    if args["command"] =="set":
        pass

    if args["command"] =="unset":
        pass

    if args["command"] =="add":
        requests_handler.add( args["name"], args["list"], args["description"], args["filters"], args["attachments"], args["information"])

    if args["command"] =="update":
        pass

    if args["command"] =="remove":
        pass

    if args["command"] =="get":
        pass

    if args['command'] == 'get':
        requests_handler.get(args['list'], args['name'], args["filters"])
    
    if args['command'] == 'logout':
        requests_handler.logout()

if __name__ == "__main__":
    main()