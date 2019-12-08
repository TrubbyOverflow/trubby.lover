FROM python:3.7

# Prevent buffering of python output that would delay console display in a docker context
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --extra-index-url https://pypi.rasa.com/simple

COPY . /app

# CMD rasa train && rasa run -m models --enable-api --log-file out.log
CMD rasa train &&\
    rasa x --no-prompt
