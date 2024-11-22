from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import os

from partition_manager import PartitionManager

app = FastAPI()
partition_manager = PartitionManager(num_partitions=3)

# Redis connection for distributed state
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

class Item(BaseModel):
    key: str
    value: str

@app.post("/items/")
async def create_item(item: Item):
    partition_manager.add_item(item.key, item.value)
    # Store in Redis for persistence
    redis_client.hset(f"partition:{partition_manager.get_partition(item.key)}", 
                     item.key, 
                     item.value)
    return {"message": "Item created", 
            "partition": partition_manager.get_partition(item.key)}

@app.get("/items/{key}")
async def read_item(key: str):
    value = partition_manager.get_item(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"key": key, "value": value, 
            "partition": partition_manager.get_partition(key)}

@app.get("/partitions/{partition_id}")
async def get_partition(partition_id: int):
    if partition_id >= partition_manager.num_partitions:
        raise HTTPException(status_code=400, 
                          detail="Invalid partition ID")
    return {"partition": partition_id, 
            "data": partition_manager.get_partition_data(partition_id)}