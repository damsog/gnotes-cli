import argparse
import requests
from utils.logger import Logger
from utils.authenticator import Authenticator
import configparser

class APIServerEndpoints:
    def __init__(self)-> None:
        self.api_base = "/api" 
        
        # Access endpoints
        self.api_base_access = f'{self.api_base}/access'
        self.login = f'{self.api_base_access}/login'
        self.create = f'{self.api_base_access}/create'

        # User endpoints
        self.api_base_user = f'{self.api_base}/user'
        self.api_user_getAll = f'{self.api_base_user}/getAll'
        self.api_user_getById = f'{self.api_base_user}/getById/:id'
        self.api_user_getByUsername = f'{self.api_base_user}/getByUsername/:username'
        self.api_user_getByEmail = f'{self.api_base_user}/getByEmail/:email'
        self.api_user_update = f'{self.api_base_user}/update/:id'
        self.api_user_delete = f'{self.api_base_user}/delete/:id'

        # List endpoints
        self.api_base_list = f'{self.api_base}/list'
        self.api_list_create = f'{self.api_base_list}/create'
        self.api_list_getAll = f'{self.api_base_list}/getAll'
        self.api_list_getByUserId = f'{self.api_base_list}/getByUserId/:id'
        self.api_list_get = f'{self.api_base_list}/get/:id'
        self.api_list_getByName = f'{self.api_base_list}/getByName/:name'
        self.api_list_update = f'{self.api_base_list}/update/:id'
        self.api_list_delete = f'{self.api_base_list}/delete/:id'


        # Object endpoints
        self.api_base_object = f'{self.api_base}/object'
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
    def __init__(self, server_url, server_port, endpoints, level="INFO") -> None:
        if level=="DEBUG":
            self.logger = Logger("DEBUG", COLORED=True)
        else:
            self.logger = Logger("INFO", COLORED=True)

        # API
        self.server_url = server_url
        self.server_port = server_port
        self.endpoints = APIServerEndpoints()

        # Configuration
        self.config = configparser.ConfigParser()
        self.config.read('config/config.init')
        self.authenticator = Authenticator()

        # List
        self.list_active = False
        self.current_list = None
    
    def login(self):
        self.logger.info("Login to the platform...")
        user = input("username: ")
        password = input("password: ")

    def create(self):
        pass

    def modify(self):
        pass

    def delete(self):
        pass

    def set(self):
        pass

    def unset(self):
        pass
    
    def add(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass

    def get(self):
        pass



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
        "get"], help="S.")
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

if __name__ == "__main__":
    main()