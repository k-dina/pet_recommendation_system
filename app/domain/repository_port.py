from typing import Protocol

from dotenv import load_dotenv

from app.domain.models import PetCreate, PetUpdate

load_dotenv()


class PetRepositoryPort(Protocol):
    """
    Interface for Pet Repository.
    Defines methods for managing pets in the system.
    """

    async def create_pet(self, pet: PetCreate) -> str:
        """Create a new pet."""
        raise NotImplementedError

    async def update_pet(self, pet_id: str, pet: PetUpdate) -> None:
        """Update an existing pet."""
        raise NotImplementedError

    async def delete_pet(self, pet_id: str) -> None:
        """Delete a pet by its ID."""
        raise NotImplementedError
