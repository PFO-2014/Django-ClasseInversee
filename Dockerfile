FROM debian
MAINTAINER Pierre Foicik <pfo.git.projects@gmail.com>

RUN apt-get update && apt-get install -y \ 
	python-pip

COPY requirements.txt /

RUN pip install --upgrade -r requirements.txt

CMD mkdir ClasseInv

COPY ClasseInversee1 /ClasseInv/
