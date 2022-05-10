from pydantic import BaseModel, Field

class PersonSchema(BaseModel):
    id: int = Field(None)
    phone: int = Field(None)
    phone_ex: str = Field(None)
    first_name: str = Field(None)
    last_name : str = Field(None)
    sex: int = Field(None)

class SocietySchema(BaseModel):
    id: str
    phone: int
    phone_ex: str
    desc: str
    location: str