from pydantic import BaseModel


class DBRecord(BaseModel):
    name: str

    class Config:
        orm_mode = True
