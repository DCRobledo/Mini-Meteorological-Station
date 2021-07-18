FROM python:3.7.3

COPY /app /etc/ur/src/app

WORKDIR /etc/ur/src/app

RUN pip install Flask Flask-Cors requests PyYAML paho-mqtt

ENTRYPOINT ["python"]
CMD ["webapp_rest_api.py"]