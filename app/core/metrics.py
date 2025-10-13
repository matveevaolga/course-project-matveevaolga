import time
from functools import wraps


def track_performance(endpoint_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            print(f"PERF: {endpoint_name} - {response_time:.2f}ms")
            return result

        return wrapper

    return decorator
