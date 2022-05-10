import models
from config import engine
from fastapi import FastAPI
from user.routes import router as user_router
from auth.routes import router as auth_router
from fastapi.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def redirect():
    return RedirectResponse("/docs")

# app.include_router(router, prefix="/book", tags=["book"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["Account"])




