FROM ubuntu:18.04
LABEL maintainer="dominik.spiljak@gmail.com"

RUN apt-get update -y && apt-get install -y build-essential cmake libsm6 libxext6 libxrender-dev python3 python3-pip python3-dev libgl1-mesa-glx

COPY ./requirements.txt /app/requirements.txt

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]