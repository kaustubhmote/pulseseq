FROM ubuntu:22.04
LABEL maintainer="Kaustubh R Mote <kaustubh.mote@gmail.com>"
LABEL image=nmrdock
LABEL tag=latest

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN dpkg --add-architecture i386 \ 
    && apt-get update -y \
    && apt-get -y install sudo \
    && apt-get -y install vim \
    && echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections \
    && apt-get -y install xterm \
    && apt-get -y install csh  \
    && apt-get -y install tcsh  \
    && apt-get -y install libx11-6:i386 \
    && apt-get -y install libxext6:i386 \
    && apt-get -y install xfonts-75dpi \
    && apt-get -y install msttcorefonts \
    && apt clean all

RUN useradd -m -d /home/nmrdock -s /bin/bash nmrdock \
    && echo "nmrdock ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/nmrdock \
    && chmod 0440 /etc/sudoers.d/nmrdock \
    && /bin/bash -c "source /home/nmrdock/.profile"

USER nmrdock
ENV HOME=/home/nmrdock

COPY nmrpipe /home/nmrdock/nmrpipe

RUN cd home/nmrdock/nmrpipe \
  && sudo chown nmrdock:nmrdock . -R \
  && chmod a+rx *.com \
  && ./install.com

RUN cd home/nmrdock/nmrpipe \
&& rm *.tZ binval.com install.com \
&& rm -r nmrbin.mac*

ENV PATH=/home/nmrdock/nmrpipe/nmrbin.linux235_64:$PATH
ENV PATH=/home/nmrdock/nmrpipe/com:$PATH
ENV PATH=/home/nmrdock/nmr_wrappers:$PATH
