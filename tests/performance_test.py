import requests
import time
import random
import concurrent.futures
import psutil
import os
from typing import List, Dict, Any
import json
from datetime import datetime
import signal
import sys

API_URL = "http://localhost:8000/message"
CONNECTION_TIMEOUT = 5.0
REQUEST_TIMEOUT = 10.0

TEST_MESSAGES = [
    "Hello, this is a test message!",
    "Testing the system performance",
    "Another test message for load testing",
    "bird-watching is fun",
    "I love mangos",
    "Someone with ailurophobia",
    "This message should pass through",
    "Load testing in progress",
    "Final test message"
]

def verify_service_availability() -> bool:
    try:
        response = requests.get(
            "http://localhost:8000/health",
            timeout=CONNECTION_TIMEOUT
        )
        if response.status_code == 200:
            health_data = response.json()
            return health_data.get("status") == "healthy"
        return False
    except requests.exceptions.RequestException as e:
        print(f"Health check failed: {str(e)}")
        return False

def send_message(message: str, user_alias: str) -> Dict[str, Any]:
    try:
        start_time = time.time()
        response = requests.post(
            API_URL,
            json={"text": message, "user_alias": user_alias},
            timeout=(CONNECTION_TIMEOUT, REQUEST_TIMEOUT)
        )
        end_time = time.time()
        
        return {
            "success": response.status_code == 200,
            "response_time": end_time - start_time,
            "status_code": response.status_code,
            "error": response.text if response.status_code != 200 else None
        }
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {str(e)}")
        return {
            "success": False,
            "response_time": 0,
            "status_code": 0,
            "error": "Connection failed - Is the API service running?"
        }
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {str(e)}")
        return {
            "success": False,
            "response_time": REQUEST_TIMEOUT,
            "status_code": 0,
            "error": "Request timed out"
        }
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return {
            "success": False,
            "response_time": 0,
            "status_code": 0,
            "error": str(e)
        }

def monitor_system_resources() -> Dict[str, float]:
    process = psutil.Process(os.getpid())
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": process.memory_percent(),
        "memory_mb": process.memory_info().rss / 1024 / 1024
    }

def run_performance_test(
    num_messages: int,
    concurrent_users: int,
    test_messages: List[str] = TEST_MESSAGES
) -> Dict[str, Any]:
    
    results = []
    system_metrics = []
    running = True
    
    def signal_handler(signum, frame):
        nonlocal running
        print("\nGracefully shutting down...")
        running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    
    def send_messages(user_id: int) -> List[Dict[str, Any]]:
        user_results = []
        messages_sent = 0
        
        while running and messages_sent < num_messages:
            message = random.choice(test_messages)
            result = send_message(message, f"tester_{user_id}")
            
            if result["success"]:
                messages_sent += 1
            elif result["error"]:
                print(f"Error sending message: {result['error']}")
            
            user_results.append(result)
            time.sleep(0.1)
        
        return user_results

    try:
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            future_to_user = {
                executor.submit(send_messages, i): i 
                for i in range(concurrent_users)
            }
            
            while running and any(not future.done() for future in future_to_user):
                system_metrics.append(monitor_system_resources())
                time.sleep(0.1)
                
            for future in concurrent.futures.as_completed(future_to_user):
                try:
                    results.extend(future.result())
                except Exception as e:
                    print(f"User task failed: {str(e)}")
        
        end_time = time.time()
        
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]
        
        if not results:
            return {"error": "No results collected"}
        
        return {
            "total_time": end_time - start_time,
            "total_requests": len(results),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "avg_response_time": sum(r["response_time"] for r in successful_requests) / len(successful_requests) if successful_requests else 0,
            "requests_per_second": len(successful_requests) / (end_time - start_time) if end_time > start_time else 0,
            "avg_cpu_percent": sum(m["cpu_percent"] for m in system_metrics) / len(system_metrics) if system_metrics else 0,
            "avg_memory_mb": sum(m["memory_mb"] for m in system_metrics) / len(system_metrics) if system_metrics else 0,
            "test_duration": end_time - start_time
        }
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        return {"error": "Test interrupted by user"}
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        return {"error": str(e)}

def main():
    print("Verifying service health...")
    retries = 3
    for attempt in range(retries):
        if verify_service_availability():
            break
        if attempt < retries - 1:
            print(f"Health check failed, retrying in 5 seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(5)
    else:
        print("Error: API service is not healthy. Please check the service status.")
        sys.exit(1)
    
    print("Service is healthy, starting tests...")
    
    scenarios = [
        (100, 1, "Test 1"),
        (100, 10, "Test 2"),
        (1000, 10, "Test 3"),
        (1000, 50, "Test 4")
    ]
    
    results = []
    
    for num_messages, concurrent_users, test_name in scenarios:
        print(f"\nStarting {test_name} test with {num_messages} messages and {concurrent_users} concurrent users...")
        
        if not verify_service_availability():
            print("Error: API service became unavailable")
            break
            
        result = run_performance_test(
            num_messages=num_messages,
            concurrent_users=concurrent_users
        )
        
        if "error" in result:
            print(f"Test failed: {result['error']}")
            break
        
        results.append({
            "test_name": test_name,
            "config": {
                "num_messages": num_messages,
                "concurrent_users": concurrent_users
            },
            "metrics": result
        })
        
        print(f"\n{test_name} Results:")
        print(f"Total time: {result['total_time']:.2f} seconds")
        print(f"Successful requests: {result['successful_requests']}")
        print(f"Failed requests: {result['failed_requests']}")
        print(f"Average response time: {result['avg_response_time']*1000:.2f} ms")
        print(f"Requests per second: {result['requests_per_second']:.2f}")
        print(f"Average CPU usage: {result['avg_cpu_percent']:.1f}%")
        print(f"Average memory usage: {result['avg_memory_mb']:.1f} MB")
    
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    main()