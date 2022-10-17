# gnotes-cli

Gnotes is an application to easily save notes, markdown info, links, and more.

This is a command line interface client to use the platform. tis client connects to a [gnotes-server](https://github.com/damsog/gnotes-server).

### Installation

To install simply clone the repository, navigate to the folder and run the install script on linux.

```sh
git clone https://github.com/damsog/gnotes-cli
cd gnotes-cli
/bin/bash install.sh
```

This will install python3.7, create a virtual environment and add it to bashrc to run it from the terminal

```sh
gno
```
```sh
Usage: gnotes.py [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  add
...
```

### Commands

|Command|Arguments   	|Description   	|Options   	|Effect   	|
|--:	|---	|--:	|--: 	|--: 	|
|create |   	|   	|*-l, --list <list_name> <br> -d, --description*|   	|
|modify |   	|   	|*-l, --list <list_name> <br> -d, --description*   	|   	|
|delete |   	|   	|*-l, --list <list_name>*   	|   	|
|set   	|*<list_name>*|   	|   	|   	|
|unset  |   	|   |   	|   	|
|add   	|*<title>*|   	|*-l, --list<br>-d, --description<br>-f, --filters<br>-a, --attachments<br>-i, --information*|   	|
|update |*<title>*|   	|*-l, --list<br>-d, --description<br>-f, --filters<br>-a, --attachments<br>-i, --information<br>-af, --add-filters<br>-aa, --add-attachments<br>-ai, --add-information<br>-rf, --remove-filters<br>-ra, --remove-attachments<br>-ri, --remove-information*   	|
|remove |*<title>*|   	|*-l, --list*  	|   	|
|get   	|   	|   	|*-l, --list<br>-n, --object-name<br>-f, --filter*|   	|
|logout |   	|   	|   	|   	|
