FROM fedora
LABEL maintainer="dominik.spiljak@gmail.com"

RUN yum update -y && yum install -y python3 python3-pip make automake gcc g++ python-devel python3-h5py

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt --user

COPY . /app
ENTRYPOINT ["python3"]
CMD ["app.py"]