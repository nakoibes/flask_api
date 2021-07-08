FROM python:3.8-alpine
WORKDIR /home/smart_tech_test_case
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY application application
COPY wsgi.py wsgi.py
EXPOSE 8000
CMD gunicorn -b 0.0.0.0 --timeout 200 "wsgi:app"