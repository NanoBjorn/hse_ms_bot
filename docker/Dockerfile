FROM python:3.8-slim

RUN mkdir /app/
COPY . /app/

WORKDIR /app/
RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]