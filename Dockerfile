FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app.py .
EXPOSE 9823
CMD ["python3", "app.py"]