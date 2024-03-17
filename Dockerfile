FROM public.ecr.aws/docker/library/python:latest


WORKDIR /srv/

RUN mkdir /data


RUN pip3 install cairosvg
RUN pip3 install numpy
RUN pip3 install colorcet
RUN pip3 install matplotlib

COPY src /srv/mathengine
COPY demo /srv/demo
COPY papers /srv/papers