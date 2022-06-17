from core.RequestHandler import RequestHandler
from libs.logger import Logger
from getpass import getpass
import argparse

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
        requests_handler.create( args["name"], 
                                 args["description"])

    if args["command"] =="modify":
        requests_handler.modify( args["name"], 
                                 args["description"])

    if args["command"] =="delete":
        requests_handler.delete( args["name"] )

    if args["command"] =="set":
        pass

    if args["command"] =="unset":
        pass

    if args["command"] =="add":
        requests_handler.add( title=args["name"], 
                              listName=args["list"], 
                              description=args["description"], 
                              filters=args["filters"], 
                              attachments=args["attachments"], 
                              information=args["information"] )

    if args["command"] =="update":
        pass

    if args["command"] =="remove":
        requests_handler.remove( name=args["name"],
                                 list=args["list"] )

    if args["command"] =="get":
        pass

    if args['command'] == 'get':
        requests_handler.get( args['list'], 
                              args['name'], 
                              args["filters"])
    
    if args['command'] == 'logout':
        requests_handler.logout()

if __name__ == "__main__":
    main()