# Webshop
Competence project to my university classes

## Virtual environment
You should use virtual environment every time you use application locally, so you don't have to care about installing Python packages. That's how you do this on Linux/macOS:
```bash
source project/bin/activate
```
And that's how to do this on Windows:
```bash
project/Scripts/activate
```

## Running server
After running server application will be available in your browser under this URL: http://127.0.0.1:8000/
```bash
python3 manage.py runserver
```

## Superuser
In order to use admin's panel, you need to create a superuser account. 
```bash
python3 manage.py createsuperuser
```
Once you did this, you can run your server and go to http://127.0.0.1:8000/admin
You need to fill the form with your superuser's login and password and then panel becomes available, so you can, for example, menage products, add new categories etc.

## Structure of project:

* project - virtual environment

* webshop - place where our applications are installed

* shop - our main application

