# Lifeguarding Website Created With Django 

Currently,this is a website created with Django to manage lifeguarding applications and employement applications. Later
it will be extended to track employees times and pools managed by the lifeguarding company.

## Getting started

### Cloning this repository
> git clone https://github.com/Jearce/lifeguard.git

### Move into repository
> cd lifeguard

### Create env
> python -m venv env

### Download requirements
> pip install -r requirements.txt

### Make migrations and migrate
```
python manage.py makemigrations
python manage.py migrate

```

### Run development server
> python manage.py runserver 

## Tests

Functional tests are written with selenium and unit tests are written with django's TestCase class. Selenium tests use [ChromeDriver](https://chromedriver.chromium.org/downloads) at the moment.

### To run tests
> python manage.py test

## Authors
* Jessie Arce

## Status of project
Still in development


