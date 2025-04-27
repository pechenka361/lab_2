FROM python:3.11.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt update && apt install -y wget && apt clean cache

COPY flask_restplus/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY flask_restplus/ /code

EXPOSE 5000

CMD ["python" "main.py"]
