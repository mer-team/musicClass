FROM python:3.6.12-slim-buster

ARG API_URL=localhost:8000
ARG HOST=localhost
ARG USER=merUser
ARG PASS=passwordMER
ARG PORT=5672
ARG MNG_PORT=15672
ARG TIME=10

COPY /src /musicClass

WORKDIR /musicClass

RUN apt-get update && apt-get install curl -y
RUN rm -rf /var/lib/apt/lists

RUN pip install -r ./requirements.txt

RUN chmod +x ./wait-for-rabbit.sh

CMD ["./wait-for-rabbit.sh", "python", "musicClassificator.py"]