from typing import Annotated, Optional

from pydantic import BaseModel, Field


class PetBase(BaseModel):
    """Pet Base Model"""

    name: str
    species: str
    age: Annotated[int, Field(ge=0)]
    temperament: str
    health: str
    sociability: str
    budget: Annotated[float, Field(gt=0.0)]


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    """All fields optional for updates"""

    name: Optional[str] = None
    species: Optional[str] = None
    age: Optional[Annotated[int, Field(ge=0)]] = None
    temperament: Optional[str] = None
    health: Optional[str] = None
    sociability: Optional[str] = None
    budget: Optional[Annotated[float, Field(gt=0.0)]] = None
