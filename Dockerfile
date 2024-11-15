FROM python:3.12-alpine
LABEL authors="ravshan"
MAINTAINER "Ravshan"
WORKDIR /app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD . .
EXPOSE 8000
CMD ["sh","-c", "python manage.py migrate; python manage.py runserver 0.0.0.0:8000"]