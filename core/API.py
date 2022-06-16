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
        self.api_list_updateByName = f'{self.api_base_list}/updateByName/:name'
        self.api_list_delete = f'{self.api_base_list}/delete/:id'
        self.api_list_deleteByName = f'{self.api_base_list}/deleteByName/:name'


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
