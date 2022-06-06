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
    args = vars(ap.parse_args())

if __name__ == "__main__":
    main()