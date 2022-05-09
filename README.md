# api.epooling.fastapi


## Virtual env
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

## OR use docker
### Env file settings
Create an .env file in root and set this params
```
DATABASE_URL=postgresql+psycopg2://postgres:password@db:5432/book_db
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=book_db 
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
POSTGRES_PASSWORD=password
```
And run docker like this
```
docker-compose build
docker-compose up
```

### Customize configuration
See [Configuration Reference](https://fastapi.tiangolo.com/).
