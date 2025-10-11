from datetime import  datetime
from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    surname: str
    lastname: str
    email: str | None
    number: str | None
    age: int
    birthday: datetime
    created_at: datetime
    active_phone: bool
    active_email: bool
    active: bool