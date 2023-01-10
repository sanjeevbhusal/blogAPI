FROM python:3.10-alpine
COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
RUN python seed_database.py
CMD ["python", "wsgi.py"]
EXPOSE 5000

