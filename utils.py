from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from config import SessionLocal, Base
from typing import Union
from fastapi import UploadFile, HTTPException, status
import uuid
import os
from os.path import join, exists
from pathlib import Path
from pydantic import BaseModel as PBaseModel


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_update_value(value: dict) -> dict:
    data_verify = {}
    for key, value in value.items():
        if value is not None:
            data_verify[key] = value
    if not data_verify.items():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update")
    return data_verify


def copy_value(
        model: Base,
        schema: PBaseModel,
        exclude=None
):
    if exclude is None:
        exclude = []
    for key, value in schema.dict().items():
        if value is not None:
            if key not in exclude:
                setattr(model, key, value)


def create_file(
        file_dir: str,
        old_file_name: Union[str, None] = None,
        file_location: Union[str, int] = '',
        file: UploadFile = '',
) -> str:
    create_dirs()
    if old_file_name is not None:
        file_path = join(Path(__file__).parent.absolute(), old_file_name)
        if exists(file_path):
            os.remove(file_path)
    file_location = f"static/{file_dir}/{file_location}_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location


def create_file_with_bytes(file_dir: str, bytes_file: bytes, file_location: str = '', file_ext: str = '', old_file_name: str = None) -> str:
    create_dirs()
    file_location = f"static/{file_dir}/{file_location}_{uuid.uuid4()}.{file_ext}"
    with open(file_location, "wb+") as file_object:
        file_object.write(bytes_file)
    if old_file_name is not None:
        print(delete_file(old_file_name))
    return file_location


def create_dirs():
    locations = ['user', 'announce']
    # Create folder if not exist
    for d in locations:
        if not exists(f'static/{d}'):
            os.makedirs(f'static/{d}')


def delete_file(file_location: str = '') -> bool:
    file_path = join(Path(__file__).parent.absolute(), file_location)
    if exists(file_path):
        os.remove(file_path)
        return True
    return False


fields_translate = {
    "id": "L'identifiant",
    "name": "Le nom",
    "first_name": "Le prénom",
    'last_name': 'Le Nom de famille',
    "email": "L'email",
    "password": "Le mot de passe",
    "phone": "Le numéro de Téléphone",
    "address": "L'adresse",
    "postal_ex": "L'extension du numéro de téléphone",
    "city": "La ville",
    "country": "Le pays",
    "birthday": "La date de naissance",
    'desc': "La description",
    'username': "Le nom d'utilisateur",
    'price': "Le prix",
    'type': "Le type",
    'order': "l'ordre",
    'is_accepted': "Accepté",
    'sex': 'Le sexe'
}
file_base64_regex = r'^data:image/[a-z]+;base64,'


