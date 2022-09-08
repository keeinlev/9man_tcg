FROM python:3.9.14-alpine
RUN apk add build-base
RUN mkdir -p /home/app
COPY . /home/app
WORKDIR /home/app
RUN apk add --no-cache supervisor \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt
CMD ["python", "run.py"]