# A Dockerfile for deloying APIServer
# To build image (in socnet directory): docker build -t socnet -f docker/Dockerfile .
# To run (in port 5000): docker run -d -p 5000:8000 socnet

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
