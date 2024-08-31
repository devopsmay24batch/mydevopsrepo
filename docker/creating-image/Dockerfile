FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY docker/creating-image/requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
