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

app.mount("/static", StaticFiles(directory="static"), name="static")


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
