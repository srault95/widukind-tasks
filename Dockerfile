FROM python:3.4.3

MAINTAINER <stephane.rault@radicalspam.org>

RUN mkdir /code

WORKDIR /code/

RUN git clone https://github.com/srault95/widukind-tasks.git \
    && cd widukind-tasks \
    && pip install -r requirements.txt \
    && pip install -e .

ENTRYPOINT ["widukind-tasks"]
CMD ["worker"]
