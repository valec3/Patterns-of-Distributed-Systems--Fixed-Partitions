from typing import List, Dict, Any
import hashlib

class PartitionManager:
    def __init__(self, num_partitions: int):
        self.num_partitions = num_partitions
        self.partitions: Dict[int, List[Any]] = {i: [] for i in range(num_partitions)}
    
    def get_partition(self, key: str) -> int:
        """Determine partition number for a given key using consistent hashing."""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_value % self.num_partitions
    
    def add_item(self, key: str, value: Any) -> None:
        """Add an item to the appropriate partition."""
        partition = self.get_partition(key)
        self.partitions[partition].append({"key": key, "value": value})
    
    def get_item(self, key: str) -> Any:
        """Retrieve an item from its partition."""
        partition = self.get_partition(key)
        for item in self.partitions[partition]:
            if item["key"] == key:
                return item["value"]
        return None
    
    def get_partition_data(self, partition: int) -> List[Dict[str, Any]]:
        """Get all data from a specific partition."""
        return self.partitions[partition]