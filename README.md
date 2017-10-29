# FlaskHasher
This is a flask vocabulary app with ability to hash words and download it on your computer.

Features:
--------

- Bootstrap 3 with Jquery for frontend
- Postgres
- Flask-SQLAlchemy
- Easy database migrations with Flask-Migrate
- Flask-WTForms for validation of form
- Unittest
- XML cast of database
- JSON downloadig
- gunicorn and nginx as server

# Getting Started

Preparing Flask modules and Environment Variables
------------------------------------------------

For first clone this repository:

` git clone https://github.com/SandPipper/FlaskHasher `

And install pyvenv:

` sudo apt-get install pyvenv `

Create virtual environment for your project:

` pyvenv-3.5 name_of_your_environment `

Edit activate script in your virtual environment:

`nano name_of_your_environment/bin/activate `


Adding to the end of file your environment variables:

```
export DATABASE_URL='postgresql://localhost/YOUR_DATABASE_NAME'
export SECRET_KEY='your_secret_key'
export ADMIN='your_mail_for_admin@gmail.com'
export MAIL_USERNAME='your_mail_for_admin@gmail.com'
export MAIL_PASSWORD='your_mail_for_admin_password'

```

Activate your virtual environment:

` source name_of_your_environment/bin/activate `

Install python packages from requirements:

` pip install -r requirements/dev.txt `


Install Postgres server and initialize data base
--------------------------------------------

Install Postgres server:

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

Create database:

```
$ sudo -u postgres psql
$ create database YOUR_DATABASE_NAME;

```
Create table with name Vocabulary:

```
$ \c YOUR_DATABASE_NAME
$ CREATE TABLE Vocabulary (
    id SERIAL PRIMARY KEY,
    word VARCHAR(255));
$ \q
```

Initialize data base and start migration script:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

To run it with gunicorn use `gunicorn --workers 3 --bind localhost manage:app --log-level debug`


Install and initialize nginx:
----------------------------

Install `sudo apt-get install nginx`


Configure it:

```
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-available/FlaskHasher
```


Put the next with edited by you path to root folder of project:

```
server {
    listen 80;
    server_name localhost;

    root /home/path/to/FlaskHasher;

    access_log /home/path/to/FlaskHasher/logs/nginx/access.log;
    error_log /home/path/to/FlaskHasher/logs/nginx/error.log;

    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
        }
    }

    location /static {
        alias /home/path/to/FlaskHasher/app/static/;
        autoindex on;
        add_header Cache-Control public;
    }

}
```


Save changes and create directory for logs:

` mkdir -p logs/nginx `


The lasts steps:

```
sudo ln -s /etc/nginx/sites-available/FlaskHasher /etc/nginx/sites-enabled/
sudo nginx -t
```


Unittests
---------
To run unittests execute next in root folder of app:

`python manage.py test`

Create XML file from database:
-----------------------------
To create XML file with information about users and their vocabularys just execute next:

But first edit manage.py and put your postgres credentials in get_info function

`python manage.py get_info`
