# Message Processing System - RabbitMQ Version

This project implements a message processing system using RabbitMQ as the message broker.

## Prerequisites

- Python 3.8+
- RabbitMQ Server
- Virtual environment (recommended)

## Installation

1. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure environment variables:

    Create a `.env` file with the following variables:

    ```plaintext
    RABBITMQ_HOST=localhost
    RABBITMQ_PORT=5672
    RABBITMQ_USER=guest
    RABBITMQ_PASS=guest
    EMAIL_SENDER=your-email@example.com
    EMAIL_PASSWORD=your-email-password
    EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com
    ```

## Running the Services

1. Start RabbitMQ server (if not already running)

2. Start each service in a separate terminal:

    ```bash
    # Terminal 1 - API Service
    python api_service/main.py

    # Terminal 2 - Filter Service
    python filter_service/main.py

    # Terminal 3 - SCREAMING Service
    python screaming_service/main.py

    # Terminal 4 - Publish Service
    python publish_service/main.py
    ```

## System Architecture

The system consists of 4 microservices:

1. **API Service**: Receives POST requests with messages and forwards them to the Filter Service
2. **Filter Service**: Filters out messages containing stop words (bird-watching, ailurophobia, mango)
3. **SCREAMING Service**: Converts messages to uppercase
4. **Publish Service**: Sends processed messages via email


## Docker Support

### Using Docker Compose (Recommended)

1. Build and start all services:

    ```bash
    docker-compose up --build
    ```

2. Access the services:
   - API Service: http://localhost:8000
   - RabbitMQ Management UI: http://localhost:15672 (guest/guest)

### Using Docker Manually

1. Build the image:

    ```bash
    docker build -t rabbitmq-version .
    ```

2. Create a Docker network:

    ```bash
    docker network create message-system
    ```

3. Start RabbitMQ:

    ```bash
    docker run -d --name rabbitmq --network message-system -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    ```

4. Start each service:

    ```bash
    # API Service
    docker run -d --name api-service --network message-system -p 8000:8000 \
      -e RABBITMQ_HOST=rabbitmq rabbitmq-version python api_service/main.py

    # Filter Service
    docker run -d --name filter-service --network message-system \
      -e RABBITMQ_HOST=rabbitmq rabbitmq-version python filter_service/main.py

    # SCREAMING Service
    docker run -d --name screaming-service --network message-system \
      -e RABBITMQ_HOST=rabbitmq rabbitmq-version python screaming_service/main.py

    # Publish Service
    docker run -d --name publish-service --network message-system \
      -e RABBITMQ_HOST=rabbitmq rabbitmq-version python publish_service/main.py
    ```

```