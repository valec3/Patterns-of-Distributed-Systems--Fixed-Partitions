import unittest
from services.partition_service import PartitionService
from models.item import Item

class TestPartitionService(unittest.TestCase):
    def setUp(self):
        self.service = PartitionService(num_partitions=3)

    def test_consistent_partitioning(self):
        """Test that the same key always maps to the same partition."""
        key = "test_key"
        partition1 = self.service.get_partition(key)
        partition2 = self.service.get_partition(key)
        self.assertEqual(partition1, partition2)

    def test_item_storage_and_retrieval(self):
        """Test adding and retrieving items."""
        item = Item(key="test_key", value="test_value")
        self.service.add_item(item)
        retrieved_item = self.service.get_item(item.key)
        self.assertEqual(item.dict(), retrieved_item.dict())

    def test_partition_distribution(self):
        """Test that items are distributed across partitions."""
        test_items = [
            Item(key=f"key{i}", value=f"value{i}")
            for i in range(4)
        ]
        
        for item in test_items:
            self.service.add_item(item)

        # Check that items exist in their assigned partitions
        for item in test_items:
            partition = self.service.get_partition(item.key)
            partition_data = self.service.get_partition_data(partition)
            self.assertTrue(
                any(i["key"] == item.key for i in partition_data)
            )