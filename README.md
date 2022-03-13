# Setup
0. What you need ahead of time
    - git
    - python
    - pip
    - npm
    - Download the .env file and make sure its named .env in the Event Horizon main folder
1. Clone the repository
    ```shell script
    cd documents/programming
    git clone https://github.com/TecKno3/EventHorizon
    ```
    - *Note* You will need to input your username and personal access token in order to clone
1. Setup python virtual environment and install python packages
    ```shell script
    cd EventHorizon
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    sudo pip3 install --default-timeout=100 -r requirements.txt
    ```
1. Install npm packages
    ```shell script
    npm install
    ```
1. Start backend and frontend
    ```shell script
    python manage.py runserver
    npm run start
    ```
Notes for failures:
comment out all django_heroku things in the settings.py file.
delete "from exec" in the manage.py file
change in requirements.txt file, python-decouple==3.1
make sure env file is there. (usually gives config or decouple errors) and named .env
include these to the ALLOWED_HOSTS in settings.py:
  'localhost',
  'localhost/',
  '127.0.0.1',
  '127.0.0.1/',

and lastly, make sure you use the url http://127.0.0.1:8080/ when going to the site.
very specific... lol
