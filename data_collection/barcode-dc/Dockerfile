FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y udev
WORKDIR /code
COPY ./requirements.txt /code/
ENV CYRPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install -r requirements.txt
COPY . /code/
