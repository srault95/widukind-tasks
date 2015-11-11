FROM python:3.4.3

MAINTAINER <stephane.rault@radicalspam.org>

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

WORKDIR /home/user

ENV PATH /opt/conda/bin:${PATH}

RUN apt-get update -y

RUN DEBIAN_FRONTEND=noninteractive \
    && wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && /bin/bash /Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && conda install -y pandas lxml numpy

RUN git clone https://github.com/Widukind/pysdmx.git \
    && cd pysdmx \
    && pip install -e .

RUN git clone https://github.com/Widukind/dlstats.git \
    && cd dlstats \
    && pip install -r requirements.txt \
    && pip install -e .

RUN git clone https://github.com/srault95/widukind-tasks.git \
    && cd widukind-tasks \
    && pip install -r requirements.txt \
    && pip install -e .

USER user

ENTRYPOINT ["widukind-tasks"]
CMD ["worker", "-l", "INFO"]
