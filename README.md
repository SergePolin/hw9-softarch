# Message Processing System

This repository contains two implementations of a message processing system:

1. [RabbitMQ Version](rabbitmq-version/README.md) - Event-driven architecture using RabbitMQ message broker
2. [Pipes and Filters Version](pipes-version/README.md) - Pipeline architecture using Python multiprocessing

## Overview

Both implementations provide the same core functionality:

- Receive text messages via REST API
- Filter out messages containing stop words
- Convert remaining messages to uppercase
- Send processed messages via email
- Log processing steps

## Performance Comparison

See [Performance Comparison](docs/performance_comparison.md) for detailed benchmarks and analysis comparing the two implementations.

## Key Differences

### RabbitMQ Version

- Microservices architecture
- Asynchronous message processing
- Better scalability and reliability
- More complex deployment
- Higher throughput and lower latency

### Pipes and Filters Version

- Single process with multiple worker pipelines
- Synchronous message processing
- Simpler deployment and debugging
- Lower resource usage
- Suitable for development/testing

## Getting Started

Choose the implementation that best fits your needs:

- [RabbitMQ Setup Guide](rabbitmq-version/README.md)
- [Pipes and Filters Setup Guide](pipes-version/README.md)
