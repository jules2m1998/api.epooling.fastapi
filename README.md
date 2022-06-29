api.epooling.fastapi
# Installation
## Env file settings
Create an ```.env``` file in root and set this params
```
DATABASE_URL=
DB_USER=
DB_PASSWORD=
DB_NAME= 
PGADMIN_EMAIL=
PGADMIN_PASSWORD=
POSTGRES_PASSWORD=

 # to jwt token auth

SECRET_KEY =
ALGORITHM = 
ACCESS_TOKEN_EXPIRE_MINUTES = 
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

## Enjoy
api docs [localhost:8000/](http://localhost:8000)  \
pgadmin [localhost:5050/](http://localhost:5050)

# Customize configuration
See [Configuration Reference](https://fastapi.tiangolo.com/).
