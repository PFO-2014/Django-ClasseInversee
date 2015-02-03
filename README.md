# Django-ClasseInversee

##1. General

A First Django project with crispy-bootstrap3
Web application to support Flipped classroom project
Build a system to support a Flipped Classroom for teachers.

see http://en.wikipedia.org/wiki/Flipped_classroom

includes:

    - Database model to support teacher materials
        - Sqlite
        - See MCD.png
    - session management that extends User from django.contrib.auth.models
    - interactive assignement for student (in progress)
    
master build from django classbook Apprendre_la_programmation_web_avec_Python_et_Django_ed1_v1

![MCD](https://github.com/PFO-2014/Django-ClasseInversee/blob/dev/ClasseInversee1/MCD.png)

2 Options for Testing/execution:

	a) Using the Django development server
	b) Using the stack NGINX <-> Unix Socket <-> WSGI <-> Django Application


##2. Installation with docker

This web application has been dockerized. 
The Dockerfile may be use to build an ad-hoc docker container:

    - Minimal debian image
    - Install all required depencies
    - Include the application

if $USER is member of docker group:

to test (*don't forget the .*)

```sh
docker build -t pfo2014/classinv:1 .
```

else, sudo all docker commands or add user to the docker group.
(http://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)

```shell
sudo gpasswd -a ${USER} docker
sudo service docker restart
```

##3. Run

Running the application can be performed:
To run and make it accessible on your localhost:8000:


### Using the Django development server:

No configuration is required just:

```shell
docker run -d -p 8000:8000 pfo2014/classinv:1  python /ClasseInv/manage.py runserver 0.0.0.0:8000
```
 - d to daemonize
 - p for tcp port forwarding


### Using the stack NGINX <-> Unix Socket <-> WSGI <-> Django Application:

need to amend the nginx conf file for path, server, host name,...:
	
	a) ClassInversee1_nginx1.conf see comments in file
	b) classeInverse_uwsgi.ini see comments in file
then:
	
```shell
docker run /etc/init.d/nginx restart && uwsgi --ini /ClasseInv/classeInverse_uwsgi.ini 
```




