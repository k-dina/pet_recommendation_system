import os
from typing import TYPE_CHECKING
from uuid import uuid4

import aioboto3
from botocore.exceptions import ClientError

from app.adapters.exceptions import NotFoundError
from app.domain.models import PetCreate, PetUpdate

if TYPE_CHECKING:
    from types_aiobotocore_dynamodb.service_resource import Table  # type: ignore


class DynamoDBPetRepository:
    """DynamoDB client for pet management"""

    _session = None
    _table_cache: dict[str, Table] = {}

    def __init__(self) -> None:
        self.table_name = os.getenv("DYNAMODB_TABLE_NAME", "Pets")

        if DynamoDBPetRepository._session is None:
            DynamoDBPetRepository._session = aioboto3.Session()

        self.session = DynamoDBPetRepository._session

    async def _get_table(self) -> Table:
        if self.table_name not in DynamoDBPetRepository._table_cache:
            async with self.session.resource("dynamodb") as dynamodb:
                DynamoDBPetRepository._table_cache[self.table_name] = dynamodb.Table(
                    self.table_name
                )
        return DynamoDBPetRepository._table_cache[self.table_name]

    async def create_pet(self, pet_data: PetCreate) -> None:
        """Create a new pet in DynamoDB. Propagates errors if any."""
        pet_id = str(uuid4())
        table = await self._get_table()
        item = {"id": pet_id, **pet_data.model_dump(exclude_none=True)}
        await table.put_item(Item=item)

    async def update_pet(self, pet_id: str, pet_update: PetUpdate) -> None:
        """Update an existing pet in DynamoDB. raises NotFoundException if
        pet not found. Propagates other errors."""
        table = await self._get_table()
        update_expression = "SET "
        expression_attribute_values = {}

        for field, value in pet_update.model_dump(exclude_none=True).items():
            update_expression += f"{field} = :{field}, "
            expression_attribute_values[f":{field}"] = value

        update_expression = update_expression.rstrip(", ")

        try:
            await table.update_item(
                Key={"id": pet_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression="attribute_exists(id)",
            )
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == "ConditionalCheckFailedException":
                raise NotFoundError(f"Pet with ID '{pet_id}' not found for update.")
            raise e

    async def delete_pet(self, pet_id: str) -> None:
        """Delete a pet from DynamoDB. Propagates errors if any."""
        table = await self._get_table()
        await table.delete_item(Key={"id": pet_id})
