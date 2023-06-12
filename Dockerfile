FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /up_apply

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY ./upworkjobapply ./


EXPOSE 8080
