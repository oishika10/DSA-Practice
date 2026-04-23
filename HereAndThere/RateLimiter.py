import time
import threading
from queue import Queue

'''
Token Bucket:
The token bucket algorithm maintains a bucket of tokens, where:

    The bucket starts with a maximum number of tokens (bucket size)
    Tokens are added to the bucket at a constant rate (tokens per second)
    When a request arrives:
        If there are enough tokens, one is consumed and the request is allowed
        If there aren’t enough tokens, the request is rejected
    The bucket never exceeds its maximum size
    This allows for burst traffic up to the bucket size, then smooths out to the refill rate
'''

class TokenBucket:
    def __init__(self, tokens_per_second: int, bucket_size: int):
        self.tokens_per_second = tokens_per_second
        self.bucket_size = bucket_size
        self.tokens = bucket_size
        self.last_refill_timestamp = time.time()
        self.lock = threading.Lock()

    def refill(self):
        now = time.time()
        elapsed_time_since_last_refill = now - self.last_refill_timestamp
        new_tokens = elapsed_time_since_last_refill * self.tokens_per_second

        with self.lock:
            self.tokens = min(self.bucket_size, self.tokens + new_tokens)
            self.last_refill_timestamp = now

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            allowed = False
            if self.tokens >= tokens:
                self.tokens -= tokens
                allowed = True
            else:
                allowed = False
            self.refill()
            return allowed

'''
The leaky bucket algorithm:

    Requests arrive at the bucket at any rate
    The bucket has a maximum capacity (queue size)
    Requests are processed at a constant rate (leak rate)
    When a request arrives:
        If there’s space in the queue, it’s added
        If the queue is full, the request is rejected
    The background thread continuously processes requests at the fixed rate

'''

class LeakyBucket:
    def __init__(self, leak_rate: int, queue_size: int):
        self.leak_rate = leak_rate
        self.queue_size = queue_size
        self.queue = Queue(maxsize=queue_size)
        self.lock = threading.Lock()
        self.processing = False
        self.stop_event = threading.Event()

    def start_processing(self):
        self.processing = True
        # 1. Create a new thread
        self.process_thread = threading.Thread(target=self.process_requests)
        #2. Start the thread
        self.process_thread.start()
        #3. Make this a daemon thread
        self.process_thread.daemon = True

    def process_requests(self):
        while not self.stop_event.is_set():
            if not self.queue.empty():
                request_id = self.queue.get()
                print(f"Processing request {request_id}")
                time.sleep(1 / self.leak_rate)  # Simulate processing time
            else:
                time.sleep(0.1)  # Sleep briefly to avoid busy waiting

    def add_request(self, request_id: int) -> bool:
        with self.lock:
            if not self.queue.full():
                self.queue.put(request_id)
                return True
            else:
                return False

    def stop_processing(self):
        if self.processing:
            self.processing = False
            self.stop_event.set()
            if hasattr(self, 'process_thread'):
                self.process_thread.join()


'''
The fixed window counter algorithm:

    Time is divided into fixed windows (e.g., 1 second)
    Each window has a maximum request limit
    When a request arrives:
        If the current window’s counter is below the limit, increment and allow
        If the counter is at the limit, reject the request
    At the start of each new window, the counter resets to zero
'''

class FixedWindowCounter:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window.size = window_size
        self.count = 0
        self.window_start = time.time()
        self.lock = threading.Lock()

    def reset_window(self):
        now = time.time()
        if now - self.window_start >= self.window_size:
            self.count = 0
            self.window_start = time.time()

    def allow_request(self) -> bool:
        with self.lock:
            self.reset_window()

            if self.count < self.limit:
                self.count += 1
                return True
            else:
                return False

'''
Sliding Window Log:

Maintains a log of all request timestamps
When a request arrives:

    Remove timestamps older than the window size
    Count remaining timestamps
    If count is below limit, add new timestamp and allow
    If count is at limit, reject the request

The window slides continuously with time
Provides exact counting within any time window
'''

class SlidingWindowLog:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        self.window_start = time.time()
        self.request_log = []
        self.lock = threading.Lock()

    def clean_old_requests(self):
        now = time.time()
        self.request_log = [timestamp for timestamp in self.request.log if now - timestamp < self.window_size]

    def allow_request(self) -> bool:
        with self.lock:
            self.clean_old_requests()

            if len(self.request_log) < self.limit:
                self.request_log.append(time.time())
                return True
            else:
                return False

'''
Sliding Window Counter:

    Maintains two counters: current window and previous window
    When a request arrives:
        Update window boundaries if needed
        Calculate weighted count from both windows
        If total is below limit, increment current window and allow
        If total is at limit, reject the request
    Uses weighted average to approximate sliding window
    Provides good accuracy with minimal memory usage
'''

class SlidingWindowCounter:
    def __init__(self, max_requests: int, window_size: int):
        """
        Initialize a sliding window counter rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_size: Size of the sliding window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.current_window = 0
        self.previous_window = 0
        self.window_start = time.time()
        self.lock = threading.Lock()

    def _reset_window(self):
        """
        Update window counters based on elapsed time.
        This method is called before each request check.
        """
        now = time.time()
        if now - self.window_start >= self.window_size:
            self.previous_window = self.current_window
            self.current_window = 0
            self.window_start = now

    def allow_request(self) -> bool:
        """
        Check if a new request is allowed using weighted counters.
        
        Returns:
            bool: True if request is allowed, False if rate limit exceeded
        """
        with self.lock:
            self._reset_window()
            current_time = time.time()
            window_progress = (current_time - self.window_start) / self.window_size
            
            # Weighted count of previous window
            weighted_count = self.previous_window * (1 - window_progress)
            total_count = weighted_count + self.current_window
            
            if total_count < self.max_requests:
                self.current_window += 1
                return True
            return False

if __name__ == "__main__":
    # Create a token bucket with 2 tokens per second and a bucket size of 5
    print("Token bucket: ")
    bucket = TokenBucket(tokens_per_second=2, bucket_size=5)

    # Simulate 20 requests
    for i in range(20):
        if bucket.consume():
            print(f"Request {i + 1}: Allowed")
        else:
            print(f"Request {i + 1}: Rejected")
        time.sleep(0.2)  # Sleep for 0.2 seconds between requests

        print("Leaky bucket:")

        bucket = LeakyBucket(rate_per_second=2, capacity=5)
        bucket.start_processing()

        try:
            # Simulate 20 requests
            for i in range(20):
                if bucket.add_request(i + 1):
                    print(f"Request {i + 1}: Added to queue")
                else:
                    print(f"Request {i + 1}: Queue full, request rejected")
                time.sleep(0.2)  # Sleep for 0.2 seconds between requests

            # Wait for all requests to be processed
            time.sleep(5)
        finally:
            bucket.stop_processing()

    print("Fixed window counter:")
    limiter = FixedWindowCounter(max_requests=5, window_size=1)

    # Simulate 20 requests
    for i in range(20):
        if limiter.allow_request():
            print(f"Request {i + 1}: Allowed")
        else:
            print(f"Request {i + 1}: Rejected")
        time.sleep(0.1)  # Sleep for 0.1 seconds between requests

    print("Sliding window log:")
    limiter = SlidingWindowLog(max_requests=5, window_size=1)

    # Simulate 20 requests
    for i in range(20):
        if limiter.allow_request():
            print(f"Request {i + 1}: Allowed")
        else:
            print(f"Request {i + 1}: Rejected")
        time.sleep(0.1)  # Sleep for 0.1 seconds between requests

    print("Sliding window counter:")
    limiter = SlidingWindowCounter(max_requests=5, window_size=1)

    # Simulate 20 requests
    for i in range(20):
        if limiter.allow_request():
            print(f"Request {i + 1}: Allowed")
        else:
            print(f"Request {i + 1}: Rejected")
        time.sleep(0.1)  # Sleep for 0.1 seconds be