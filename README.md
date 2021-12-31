# Setup
0. What you need ahead of time
    - git
    - python
    - pip
    - npm
1. Clone the repository
    ```shell script
    cd documents/programming
    git clone h
    ```
    - *Note* You will need to input your username and personal access token in order to clone
1. Setup python virtual environment and install python packages
    ```shell script
    cd EventHorizon
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install --default-timeout=100 -r requirements.txt
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
