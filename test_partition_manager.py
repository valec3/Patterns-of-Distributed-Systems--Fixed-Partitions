import unittest
from partition_manager import PartitionManager

class TestPartitionManager(unittest.TestCase):
    def setUp(self):
        self.manager = PartitionManager(num_partitions=3)

    def test_consistent_partitioning(self):
        """Test that the same key always maps to the same partition."""
        key = "test_key"
        partition1 = self.manager.get_partition(key)
        partition2 = self.manager.get_partition(key)
        self.assertEqual(partition1, partition2)

    def test_item_storage_and_retrieval(self):
        """Test adding and retrieving items."""
        key = "test_key"
        value = "test_value"
        self.manager.add_item(key, value)
        retrieved_value = self.manager.get_item(key)
        self.assertEqual(value, retrieved_value)

    def test_partition_distribution(self):
        """Test that items are distributed across partitions."""
        test_data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
            "key4": "value4"
        }
        
        for key, value in test_data.items():
            self.manager.add_item(key, value)

        # Check that items exist in their assigned partitions
        for key, value in test_data.items():
            partition = self.manager.get_partition(key)
            partition_data = self.manager.get_partition_data(partition)
            self.assertTrue(any(item["key"] == key for item in partition_data))

if __name__ == '__main__':
    unittest.main()