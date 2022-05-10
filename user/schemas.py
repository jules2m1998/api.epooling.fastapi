from pydantic import BaseModel

class PersonSchema(BaseModel):
    id: int = None
    phone: int = None
    phone_ex: str = None
    first_name: str = None
    last_name : str = None
    sex: int = None

class SocietySchema(BaseModel):
    id: str
    phone: int
    phone_ex: str
    desc: str
    location: str