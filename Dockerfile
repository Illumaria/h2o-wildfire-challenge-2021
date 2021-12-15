FROM python:3.8.12-slim

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get -y install libgomp1

COPY . /usr/src/app
RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 4400

CMD ["python", "app.py"]