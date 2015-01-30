# Django-ClasseInversee

##1. General

Running the application can be performed using the Django development server.

Web application to support Flipped classroom project

A First Django project with crispy-bootstrap3

Build a system to support a Flipped Classroom for teachers.

see http://en.wikipedia.org/wiki/Flipped_classroom

includes:

    - Database model to support teacher materials
        - Sqlite
        - See MCD.png
    - session management that extends User from django.contrib.auth.models
    - interactive assignement for student (in progress)
    

master build from django classbook Apprendre_la_programmation_web_avec_Python_et_Django_ed1_v1

##2. Installation with docker

This web application has been dockerized. 
The Dockerfile may be use to build an ad-hoc docker container:

    - Minimal debian image
    - Install all required depencies
    - Include the application

to test (*don't forget the .*)

```sh
docker build -t pfo2014/classinv:1 .
```

##3. Run

To run it a make it accessible on your localhost:8000:
 - d to daemonize
 - p for tcp port forwarding

```shell
docker run -d -p 8000:8000 pfo2014/classinv:1  python /ClasseInv/manage.py runserver 0.0.0.0:8000
```


