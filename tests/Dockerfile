FROM docker:latest
RUN apk add --no-cache py-pip
RUN mkdir /tests
WORKDIR /tests
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 