from pydantic import BaseModel

class BaseEntity(BaseModel):

    class Config:
        
        from_attributes = True