FROM python:3.8-slim

RUN mkdir /app/
COPY requirements.txt /app/
WORKDIR /app/
RUN sudo apt-get install libpq-dev
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]