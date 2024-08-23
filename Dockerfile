FROM python:3.12-alpine
LABEL authors="ravshan"
MAINTAINER "Ravshan"
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
RUN sed -i 's/^DEBUG=.*/DEBUG="0"/' .env
EXPOSE 8000
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]