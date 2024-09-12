FROM python:3.12-alpine
LABEL authors="ravshan"
MAINTAINER "Ravshan"
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
#RUN sed -i 's/^DEBUG=.*/DEBUG="0"/' .env
#RUN sed -i 's/^DB_HOST=.*/DB_HOST="leo.ravshandev.uz"/' .env
EXPOSE 8000
CMD ["sh","-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]