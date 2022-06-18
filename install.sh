sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
python3 -m pip install virtualenv
virtualenv gnotes_venv --python=python3.7
source gnotes_venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install requests
python3 -m pip install python-dotenv
python3 -m pip install colorful
python3 -m pip install configparser
python3 -m pip install rich
python3 -m pip install click
