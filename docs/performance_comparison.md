# Performance Comparison: RabbitMQ vs Pipes-and-Filters

We compare the performance of the two message processing system implementations:

1. Event-driven system using RabbitMQ
2. Pipes-and-filters architecture using Python multiprocessing

## System Configurations

Both systems were tested on the same hardware:

- Intel Core i5 (2 cores, 4 threads) - MacBook Pro 2019 13-inch
- 8GB RAM
- macOS

## Test Scenarios

We tested both implementations under the scenarios:

1. Light load: 100 messages, 1 concurrent user
2. Medium load: 100 messages, 10 concurrent users
3. Heavy load: 1000 messages, 10 concurrent users
4. Stress test: 1000 messages, 50 concurrent users

## Performance Metrics

### Light Load (100 messages, 1 user)

| Metric | RabbitMQ | Pipes-and-Filters |
|--------|----------|-------------------|
| Throughput (msg/s) | 8.26 | 4.66 |
| Avg Response Time (ms) | 17.76 | 110.54 |
| CPU Usage (%) | 41.57 | 28.21 |
| Memory Usage (MB) | 19.93 | 16.56 |
| Success Rate (%) | 100 | 100 |

### Medium Load (100 messages, 10 users)

| Metric | RabbitMQ | Pipes-and-Filters |
|--------|----------|-------------------|
| Throughput (msg/s) | 67.22 | 9.21 |
| Avg Response Time (ms) | 41.05 | 977.58 |
| CPU Usage (%) | 39.40 | 22.19 |
| Memory Usage (MB) | 19.17 | 17.52 |
| Success Rate (%) | 100 | 100 |

### Heavy Load (1000 messages, 10 users)

| Metric | RabbitMQ | Pipes-and-Filters |
|--------|----------|-------------------|
| Throughput (msg/s) | 75.65 | 8.72 |
| Avg Response Time (ms) | 26.66 | 1039.48 |
| CPU Usage (%) | 34.58 | 29.26 |
| Memory Usage (MB) | 22.53 | 18.78 |
| Success Rate (%) | 100 | 100 |

### Stress Test (1000 messages, 50 users)

| Metric | RabbitMQ | Pipes-and-Filters |
|--------|----------|-------------------|
| Throughput (msg/s) | 153.09 | 8.29 |
| Avg Response Time (ms) | 217.44 | 5468.71 |
| CPU Usage (%) | 48.30 | 27.00 |
| Memory Usage (MB) | 32.67 | 25.15 |
| Success Rate (%) | 100 | 63.56 |

## Analysis

### Time Behavior

- **RabbitMQ** shows significantly better response times across all scenarios.
- **Pipes-and-Filters** response times degrade more rapidly under load.

RabbitMQ maintains consistent throughput scaling, while Pipes-and-Filters throughput remains relatively flat.

### Resource Utilization

- **CPU Usage**: RabbitMQ shows higher but more consistent CPU utilization
- **Memory Usage**: Both implementations show modest memory footprint
- RabbitMQ scales better with increased load
- Pipes-and-Filters shows lower resource usage but also lower performance

### Capacity

- **RabbitMQ**:
  - Scales well with concurrent users
  - Maintains high success rate under stress
  - Throughput increases with load
- **Pipes-and-Filters**:
  - Limited scalability with concurrent users
  - Significant degradation under stress
  - High failure rate in stress test (36.44%)

## Conclusions

1. **Scalability**: RabbitMQ scales much better and handles multiple users at the same time with ease.

2. **Reliability**: RabbitMQ maintains 100% success rate across all tests, while Pipes-and-Filters shows significant failures under stress.

3. **Performance**:
   - RabbitMQ achieves 5-18x higher throughput
   - RabbitMQ response times are 5-25x faster
   - RabbitMQ handles concurrent load more gracefully

4. **Resource Efficiency**: While Pipes-and-Filters uses fewer resources, it achieves this at the cost of significantly lower performance.

## Recommendations

1. **Production Usage**:
   - Use RabbitMQ implementation for production workloads
   - Especially important for scenarios requiring:
     - High throughput
     - Concurrent user support
     - Reliable message delivery

2. **Development/Testing**:
   - Pipes-and-Filters may be suitable for development/testing
   - Simpler to deploy and debug
   - Adequate for low-volume, single-user scenarios

3. **Improvements**:
   - Pipes-and-Filters could be improved by:
     - Implementing better concurrency handling
     - Adding message buffering
     - Optimizing inter-process communication
   - RabbitMQ could be improved by:
     - Fine-tuning resource usage
     - Implementing message batching for better efficiency
