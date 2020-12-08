FROM fedora
LABEL maintainer="dominik.spiljak@gmail.com"

RUN yum update -y && yum install -y build-essential cmake libsm6 libxext6 libxrender-dev python3 python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
ENTRYPOINT ["python3"]
CMD ["app.py"]