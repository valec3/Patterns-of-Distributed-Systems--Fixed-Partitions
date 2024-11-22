# Fixed Partitions Pattern Implementation

This project implements the Fixed Partitions pattern for distributed systems using Python, FastAPI, and Redis.

## Features

- Consistent hashing for partition assignment
- Multiple partition nodes
- Redis for distributed state management
- REST API for data operations
- Docker containerization

## API Endpoints

- `POST /items/`: Create a new item
- `GET /items/{key}`: Retrieve an item by key
- `GET /partitions/{partition_id}`: Get all items in a partition

## Running the Project

1. Start the containers:
   ```bash
   docker-compose up --build
   ```

2. Access the services:
   - Partition 1: http://localhost:8001
   - Partition 2: http://localhost:8002
   - Partition 3: http://localhost:8003

## Testing

Run the tests:
```bash
python -m unittest test_partition_manager.py
```