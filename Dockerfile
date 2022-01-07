FROM python:latest


WORKDIR /srv/

RUN mkdir /data


RUN pip3 install cairosvg
RUN pip3 install numpy
RUN pip3 install colorcet 

COPY src /srv/mathengine
COPY demo /srv/demo
