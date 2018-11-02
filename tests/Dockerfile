FROM docker:latest
RUN apk add --no-cache py-pip
RUN mkdir /tests
COPY requirements.txt ./tests
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 