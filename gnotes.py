import argparse
import requests
from utils.logger import Logger

class RequestHandler:
    def __init__(self, server_url, server_port, level="INFO") -> None:
        if level=="DEBUG":
            self.logger = Logger("DEBUG", COLORED=True)
        else:
            self.logger = Logger("INFO", COLORED=True)

        self.server_url = server_url
        self.server_port = server_port

        self.api_name = "/api"
    
    def login(self):
        login_endpoint = "/access/login"
        self.logger.info("Login to the platform...")
        user = input("username: ")
        password = input("password: ")


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

    logger.info(" Printing Test")

if __name__ == "__main__":
    main()