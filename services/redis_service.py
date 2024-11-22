import redis
import os
from typing import Optional

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
    
    def store_item(self, partition_id: int, key: str, value: str) -> None:
        self.client.hset(f"partition:{partition_id}", key, value)
    
    def get_item(self, partition_id: int, key: str) -> Optional[str]:
        return self.client.hget(f"partition:{partition_id}", key)
    
    def get_partition_data(self, partition_id: int) -> dict:
        return self.client.hgetall(f"partition:{partition_id}")