# Dockerfile-flask
# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:alpine
RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		git \
		gcc \
		libc-dev \
		linux-headers \
	;
RUN git clone https://github.com/requests/requests.git; \
	cd requests; \
	pip install -U pip; \
	pip install .;
## Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir /webapp
WORKDIR /webapp
# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .
# Install Python dependencies
RUN pip install -r requirements.txt
# Delete .build-deps
RUN apk del .build-deps;
# We copy the rest of the codebase into the image
COPY . .
# Run uwsgi unprivileged
RUN addgroup -S uwsgi && adduser -S uwsgi -G uwsgi
# Finally, we run uWSGI with the ini file we
# created earlier
CMD [ "uwsgi", "--ini", "webapp.ini" ]