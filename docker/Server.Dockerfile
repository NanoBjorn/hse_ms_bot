FROM ubuntu:latest

RUN mkdir /app/
COPY requirements.txt /app/
WORKDIR /app/
RUN apt-get update
RUN yes | apt-get install libpq-dev python3-pip
RUN pip3 install -r requirements.txt
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:/src"
CMD ["python3", "src/server/main.py"]