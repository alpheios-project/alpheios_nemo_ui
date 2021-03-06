FROM python:3.6.8-alpine

# Install required packages
RUN apk add --no-cache \
        gcc linux-headers libxml2 libxml2-dev libxslt libxslt-dev musl musl-dev unzip curl libffi-dev openssl-dev nodejs nodejs-npm git

# Sets up locales to avoid decode issue in python
ENV LANG C.UTF-8
ARG appkey=mysecret
ARG clientid=iT75HkBHThA4QdFwFoZRofLC41vVyvAt
ARG clientsecret=8BgJVs5sgyI5w10hXTY-D4Dv-HoCy-DxnXHJYDFISwX47wwtsK5oqboNmAhWBFQ3
ARG proxybase=http://dev.alpheios.net:5000

WORKDIR /code/
ADD ./requirements.txt requirements.txt
ADD ./app.py app.py
RUN pip3 install -r requirements.txt

VOLUME ["/code/alpheios_nemo_ui", "/code/texts"]

# Expose right ports
EXPOSE 5000

ENV ALPHEIOS_NEMO_APPKEY=${appkey}
ENV ALPHEIOS_NEMO_AUTH0_CLIENTID=${clientid}
ENV ALPHEIOS_NEMO_AUTH0_CLIENTSECRET=${clientsecret}
ENV ALPHEIOS_NEMO_PROXYBASE=${proxybase}

RUN chmod 644 app.py
CMD ["python", "app.py"]
