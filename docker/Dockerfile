# A Dockerfile for deloying APIServer

FROM python:3.7

COPY requirements/requirements.txt /requirements.txt
COPY requirements/requirements-dev.txt /requirements-dev.txt
COPY makefile makefile
COPY APIServer/ APIServer/

RUN pip install --upgrade pip

RUN pip install -r requirements-dev.txt
RUN pip install -r requirements.txt

ENV PYTHONPATH "pwd"

CMD ["make", "api_server"]
