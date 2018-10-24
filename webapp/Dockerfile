# Dockerfile-flask
# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:alpine
RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	;
# Set an environment variable with the directory
# where we'll be running the WEBAPP
ENV WEBWEBAPP /webapp
# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $WEBAPP
WORKDIR $WEBAPP
# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .
# Install Python dependencies
RUN pip install --upgrade pip
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