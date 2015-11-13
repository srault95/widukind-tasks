FROM debian:jessie

ENV LANG C.UTF-8
ENV PATH /opt/conda/bin:${PATH}
ENV PYTHON_RELEASE 3.4.3

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN apt-get update -y

WORKDIR /home/user

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  ca-certificates \
  curl \
  wget \
  git \
  bzip2
    
RUN wget -O /tmp/miniconda3.sh --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && /bin/bash /tmp/miniconda3.sh -b -p /opt/conda \
    && conda install python=$PYTHON_RELEASE \
    && conda remove -y pycrypto \
    && conda clean -y -i -l -t -p -s \
    && conda install -y pandas lxml numpy numexpr Bottleneck beautifulsoup4 xlrd \
    && rm -f /tmp/miniconda3.sh

#TODO: release ?
#TODO: directory ?
RUN git clone https://github.com/Widukind/pysdmx.git \
    && cd pysdmx \
    && pip install -e .

RUN git clone https://github.com/Widukind/dlstats.git \
    && cd dlstats \
    && pip install -r requirements.txt \
    && pip install -e .

ADD . /code/

WORKDIR /code/

RUN pip install -r requirements-docker.txt \
    && pip install -r requirements-tests.txt \
    && pip install --no-deps -e .

USER user

ENTRYPOINT ["widukind-tasks"]

CMD ["worker", "-l", "INFO"]
