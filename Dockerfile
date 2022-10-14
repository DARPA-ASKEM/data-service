FROM python:latest
RUN apt update 2> /dev/null
RUN apt install -y postgresql postgresql-contrib
WORKDIR /api
ADD requirements.txt requirements.txt
ADD askem.dbml askem.dbml
RUN pip install -r requirements.txt
COPY src src 
EXPOSE 8000
WORKDIR /api/src
CMD ["./main.py", "start", "admin", "projects"]
