<h3 align="center">London Economic Today API</h3>
<p align="center">
    <br/>
    <a href="https://www.python.org"
    ><img
            src="https://img.shields.io/badge/Python-v3.12-blue.svg?longCache=true&logo=python&style=for-the-badge&logoColor=white&colorB=5e81ac&colorA=4c566a"
            alt="Python 3.12"
    /></a>
    <a href="https://flask.palletsprojects.com"
    ><img
            src="https://img.shields.io/badge/Flask-v3.0.3-blue.svg?longCache=true&logo=flask&style=for-the-badge&logoColor=white&colorB=5e81ac&colorA=4c566a"
            alt="Flask"
    /></a>
    <a href="https://gunicorn.org"
    ><img
            src="https://img.shields.io/badge/Gunicorn-v21.2.0-blue.svg?longCache=true&logo=gunicorn&style=for-the-badge&logoColor=white&colorB=a3be8c&colorA=4c566a"
            alt="Gunicorn"
    /></a>
    <br/>
</p>

## Getting Started

1. Create a virtual environment & install dependencies

   ```
   conda create -n london_eco_today python=3.12
   conda activate london_eco_today
   pip install -r requirements.txt
   ```

2. Run the **development server**

   ```
   flask --app app run
   ```

3. Access the testing API: http://127.0.0.1:5000/api/v1/hello

## Deploying to Production

### Docker

```
docker run -d -p 8000:8000 --name london_eco_today_api --restart=always teiiri/london_eco_today_api:latest
```

### Docker Compose

```yaml
services:
  london_eco_today_api:
    container_name: london_eco_today_api
    image: teiiri/london_eco_today_api:latest
    restart: always
    ports:
      - "8000:8000"
```

