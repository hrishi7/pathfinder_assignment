from python:3.11.0a6-alpine3.15
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 5000
COPY . /app
CMD python main.py