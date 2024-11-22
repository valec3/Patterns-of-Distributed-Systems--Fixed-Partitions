from typing import List, Dict, Any, Optional
import hashlib
from models.item import Item

class PartitionService:
    def __init__(self, num_partitions: int):
        self.num_partitions = num_partitions
        self.partitions: Dict[int, List[Dict[str, Any]]] = {
            i: [] for i in range(num_partitions)
        }
    
    def get_partition(self, key: str) -> int:
        """Determine partition number for a given key using consistent hashing."""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_value % self.num_partitions
    
    def add_item(self, item: Item) -> int:
        """Add an item and return its partition number."""
        partition = self.get_partition(item.key)
        self.partitions[partition].append(item.dict())
        return partition
    
    def get_item(self, key: str) -> Optional[Item]:
        """Retrieve an item by its key."""
        partition = self.get_partition(key)
        for item in self.partitions[partition]:
            if item["key"] == key:
                return Item(**item)
        return None
    
    def get_partition_data(self, partition_id: int) -> List[Dict[str, Any]]:
        """Get all items in a partition."""
        if partition_id >= self.num_partitions:
            raise ValueError("Invalid partition ID")
        return self.partitions[partition_id]