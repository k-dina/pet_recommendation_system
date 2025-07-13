import logging
import os

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status

from app.adapters.exceptions import NotFoundError
from app.adapters.repository import DynamoDBPetRepository
from app.domain.models import PetCreate, PetUpdate

# Configure logging with detailed timestamp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def get_pet_repository() -> DynamoDBPetRepository:
    """Initialize and return the pet repository"""
    return DynamoDBPetRepository()


app = FastAPI(
    title="Pet Recommendation System API",
    description="A FastAPI application for managing pets with DynamoDB",
    version="1.0.0",
)


@app.get("/", response_model=dict)
async def root() -> dict:
    """Root endpoint"""
    return {
        "message": "Welcome to Pet Recommendation System API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=dict)
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "pet-recommendation-system"}


@app.post("/pets", status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_data: PetCreate,
    pet_repository: DynamoDBPetRepository = Depends(get_pet_repository),
) -> None:
    """Create a new pet"""
    try:
        await pet_repository.create_pet(pet_data)
    except Exception as e:
        logger.error(f"Error creating pet: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.put("/pets/{pet_id}", status_code=status.HTTP_200_OK)
async def update_pet(
    pet_id: str,
    pet_update: PetUpdate,
    pet_repository: DynamoDBPetRepository = Depends(get_pet_repository),
) -> None:
    """Update a pet"""
    try:
        await pet_repository.update_pet(pet_id, pet_update)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found"
        )
    except Exception as e:
        logger.error(f"Error updating pet: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.delete("/pets/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(
    pet_id: str, pet_repository: DynamoDBPetRepository = Depends(get_pet_repository)
) -> None:
    """Delete a pet"""
    try:
        await pet_repository.delete_pet(pet_id)
    except Exception as e:
        logger.error(f"Error deleting pet: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def main() -> None:
    """Run the FastAPI application"""
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")  # nosec B104

    uvicorn.run("main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    main()
