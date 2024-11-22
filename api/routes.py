from fastapi import APIRouter, HTTPException
from models.item import Item
from services.partition_service import PartitionService
from services.redis_service import RedisService

router = APIRouter()
partition_service = PartitionService(num_partitions=3)
redis_service = RedisService()

@router.post("/items/")
async def create_item(item: Item):
    partition = partition_service.add_item(item)
    redis_service.store_item(partition, item.key, item.value)
    return {
        "message": "Item created",
        "partition": partition
    }

@router.get("/items/{key}")
async def read_item(key: str):
    item = partition_service.get_item(key)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "key": item.key,
        "value": item.value,
        "partition": partition_service.get_partition(key)
    }

@router.get("/partitions/{partition_id}")
async def get_partition(partition_id: int):
    try:
        data = partition_service.get_partition_data(partition_id)
        return {
            "partition": partition_id,
            "data": data
        }
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid partition ID"
        )