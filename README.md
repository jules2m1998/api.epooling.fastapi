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
```
docker-compose build
docker-compose up
```

### Customize configuration
See [Configuration Reference](https://fastapi.tiangolo.com/).
