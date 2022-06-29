from config import engine
from fastapi import FastAPI
from user.routes import router as user_router
from user.models import Base
from auth.routes import router as auth_router
from announce.routes import router as announce_router, cityRouter as city_router
from itinerary.routes import router as itinerary_router
from order.routes import router as order_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse
import json
from typing import Union
from utils import fields_translate

Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Handle exceptions
@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: Union[RequestValidationError, ValidationError]):
    print(exc, 'exc')
    try:
        print(f"OMG! The client sent invalid data!: {exc}")
        exc_json = json.loads(exc.json())
        response = {"detail": []}
        print(exc_json)

        for error in exc_json:
            field: str = str(error["loc"][-1]).lower()
            translate: str = fields_translate.get(field)
            print('field: ', field)
            print('translate: ', translate)
            message = ''
            typer, value = error["type"].split('.')
            if translate:
                field = translate.capitalize()
            else:
                field = field.replace("_", " ").capitalize()
            if'type_error' in typer:
                if 'integer' in value:
                    message = f"{field} doit être un nombre entier"
                elif 'string' in value:
                    message = f"{field} doit être une chaîne de caractères"
                elif 'boolean' in value:
                    message = f"{field} doit être un booléen"
                else:
                    message = f"{field} n'est pas dubon type"
            elif 'value_error' in typer:
                if 'missing' in value:
                    message = f"{field} est obligatoire"
            else:
                message = error['msg']
            response['detail'].append({
                'fieldTrans': field,
                'message': message,
                'field': str(error["loc"][-1]).lower()
            })
            print(response)
    except Exception as e:
        print(isinstance(e, ValueError))
        if isinstance(e, ValueError):
            response = {"detail": [{"message": "Veillez remplir tous les champs !", "field": "all"}]}
        else:
            response = {"detail": [{"fieldTrans": "", "message": "Une erreur s'est produite", "field": "all"}]}
    return JSONResponse(response, status_code=422)


@app.get('/')
def redirect():
    return RedirectResponse("/docs")


# app.include_router(router, prefix="/book", tags=["book"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["Account"])
app.include_router(announce_router, prefix="/announce", tags=["Announce"])
app.include_router(city_router, prefix="/city", tags=["City"])
app.include_router(itinerary_router, prefix="/itinerary", tags=["Itinerary"])
app.include_router(order_router, prefix="/order", tags=["Order"])
