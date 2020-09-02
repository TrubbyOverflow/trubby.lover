FROM python:3.7

# Prevent buffering of python output that would delay console display in a docker context
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

RUN rasa train

CMD rasa run
