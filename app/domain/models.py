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


class Pet(PetBase):
    """Pet response model with ID"""

    id: str

    class Config:
        from_attributes = True


class PetResponse(BaseModel):
    """Standard response wrapper"""

    success: bool
    message: str
    data: Optional[Pet] = None


class PetListResponse(BaseModel):
    """Response for listing pets"""

    success: bool
    message: str
    data: list[Pet] = []
    count: int = 0
