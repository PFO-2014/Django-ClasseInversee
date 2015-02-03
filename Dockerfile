FROM debian

MAINTAINER Pierre Foicik <pfo.git.projects@gmail.com>

RUN apt-get update && apt-get install -y \
	build-essential \
	python-dev \
	python-pip \
	nginx \
	git

# Reference requirements
COPY requirements.txt /
RUN pip install --upgrade -r requirements.txt

# Install our code
CMD mkdir /home/site
COPY ClasseInversee1 /home/site

#Add user to group www-data for nginx
#RUN usermod -a -G www-data $USER 

# Setup all the configfiles
# simlink so nginx can see the ad-hoc conf. file
RUN ln -s /home/site/ClasseInversee1_nginx.conf /etc/nginx/sites-enabled/
# Make sure all static/media files permissions are allowing read
RUN chmod -R +rw /home/site/static  
RUN chmod -R +rw /home/site/media


# Expose Django application private port: ClasseInverse1
EXPOSE 8000
