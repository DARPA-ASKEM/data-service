FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
ADD askem.dbml askem.dbml
RUN pip install -r requirements.txt
COPY src src 
EXPOSE 8000
WORKDIR /code/src
CMD ["./main.py", "start", "admin", "projects"]
