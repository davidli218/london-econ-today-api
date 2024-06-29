FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

EXPOSE 8000

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()" ]
