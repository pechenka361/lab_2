FROM python:3.11.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt update && apt install -y wget && apt clean cache

COPY flask_app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY flask_app/ /code

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "main:app"]
