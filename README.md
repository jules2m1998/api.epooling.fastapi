api.epooling.fastapi
# Installation
## Env file settings
Create an .env file in root and set this params
```
DATABASE_URL=
DB_USER=
DB_PASSWORD=
DB_NAME= 
PGADMIN_EMAIL=
PGADMIN_PASSWORD=
POSTGRES_PASSWORD=
```
## Simple installation
### Virtual env
```
python3 -m venv venv
source venv/bin/activate
```

### Install requirement lib
```
pip install -r requirements.txt
```

### Run fastapi server
```
uvicorn main:app --reload
```

## Docker installation
Just run docker like this
```
docker-compose build
docker-compose up
```

# Customize configuration
See [Configuration Reference](https://fastapi.tiangolo.com/).
