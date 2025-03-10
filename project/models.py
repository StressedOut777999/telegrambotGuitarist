from pydantic import BaseModel
from aiogram.fsm.state import State, StatesGroup

class Instruments(BaseModel):
    name: str
    img: str
    song: str

class Guitarists_info(BaseModel):
    name: str
    instruments: list[Instruments]
    description: str
    


