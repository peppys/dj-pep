FROM python:3.7.2

LABEL description="dj-pep-api"

RUN mkdir -p /opt/app

ADD api /opt/app/api
ADD lib /opt/app/lib

ADD main.py /opt/app
ADD requirements.txt /opt/app

WORKDIR /opt/app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "./main.py"]
