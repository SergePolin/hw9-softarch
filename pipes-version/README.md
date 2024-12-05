# Pipes and Filters Implementation

This implementation uses Python's multiprocessing to create a pipeline of filters that process messages sequentially.

## Prerequisites

- Python 3.8+
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Architecture

The system consists of three main components:

1. **Filter Base Class**: Abstract base class that defines the filter interface
2. **Processing Filters**:
   - ScreamingFilter: Converts text to uppercase
   - ProfanityFilter: Censors specified bad words
   - EmailFilter: Sends processed messages via email
3. **Pipeline**: Connects filters using multiprocessing Queues

## Usage

### Running the API Server

```bash
python3 pipes-version/api.py
```

The server will start on <http://localhost:8000>

### API Endpoints

- POST /message - Process a message

- GET /health - Check server health

### Running Performance Tests

```bash
python3 tests/performance_test.py
```

## Docker Support

### Using Docker Compose (Recommended)

1. Build and start the service:

```bash
docker-compose up --build
```

2. Access the API at http://localhost:8000

### Using Docker Manually

1. Build the image:

```bash
docker build -t pipes-version .
```

2. Run the container:

```bash
docker run -d -p 8000:8000 pipes-version
```