FROM python:3.7-alpine

RUN pip install paho-mqtt
RUN pip install requests

ADD alohomora.py / 

CMD [ "python", "./alohomora.py" ]


