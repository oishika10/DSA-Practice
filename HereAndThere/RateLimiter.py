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
        If there aren't enough tokens, the request is rejected
    The bucket never exceeds its maximum size
    This allows for burst traffic up to the bucket size, then smooths out to the refill rate
'''

class TokenBucket:
    def __init__(self, tokens_per_second: int, bucket_size: int):
        self.tokens_per_second = tokens_per_second
        self.bucket_size = bucket_size
        # Start full so the first burst of requests up to bucket_size are all allowed immediately
        # e.g. bucket_size=5 → first 5 requests pass with no wait
        self.tokens = bucket_size
        self.last_refill_timestamp = time.time()
        # Lock needed because refill() and consume() can be called from different threads simultaneously
        self.lock = threading.Lock()

    def refill(self):
        now = time.time()
        # How many seconds have passed since we last added tokens?
        # e.g. tokens_per_second=2, elapsed=0.5s → new_tokens = 1.0
        elapsed_time_since_last_refill = now - self.last_refill_timestamp
        new_tokens = elapsed_time_since_last_refill * self.tokens_per_second

        with self.lock:
            # Cap at bucket_size so tokens never overflow the bucket
            # e.g. tokens=4, new_tokens=3, bucket_size=5 → tokens = min(5, 7) = 5
            self.tokens = min(self.bucket_size, self.tokens + new_tokens)
            self.last_refill_timestamp = now

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            allowed = False
            if self.tokens >= tokens:
                # Enough tokens available — deduct and allow the request
                # e.g. self.tokens=3, tokens=1 → self.tokens becomes 2, allowed=True
                self.tokens -= tokens
                allowed = True
            else:
                # Not enough tokens — reject without changing the count
                # e.g. self.tokens=0, tokens=1 → bucket empty, allowed=False
                allowed = False
            # Refill after each consume so tokens accumulate between requests
            self.refill()
            return allowed

'''
The leaky bucket algorithm:

    Requests arrive at the bucket at any rate
    The bucket has a maximum capacity (queue size)
    Requests are processed at a constant rate (leak rate)
    When a request arrives:
        If there's space in the queue, it's added
        If the queue is full, the request is rejected
    The background thread continuously processes requests at the fixed rate

'''

class LeakyBucket:
    def __init__(self, leak_rate: int, queue_size: int):
        self.leak_rate = leak_rate
        self.queue_size = queue_size
        # Bounded queue enforces the capacity limit — putting to a full queue raises an exception
        # e.g. queue_size=5 means at most 5 requests can be waiting at once
        self.queue = Queue(maxsize=queue_size)
        self.lock = threading.Lock()
        self.processing = False
        # Event flag used to signal the background thread to stop gracefully
        self.stop_event = threading.Event()

    def start_processing(self):
        self.processing = True
        # 1. Create a new thread that runs process_requests in the background
        self.process_thread = threading.Thread(target=self.process_requests)
        # 2. Start the thread
        self.process_thread.start()
        # 3. Mark as daemon so it dies automatically if the main program exits
        #    without needing an explicit stop_processing() call
        self.process_thread.daemon = True

    def process_requests(self):
        # Keep looping until stop_processing() sets the stop_event flag
        while not self.stop_event.is_set():
            if not self.queue.empty():
                # Pull the next request off the front of the queue (FIFO order)
                request_id = self.queue.get()
                print(f"Processing request {request_id}")
                # Sleep to enforce the fixed output rate
                # e.g. leak_rate=2 → sleep 0.5s between each request → 2 requests/second max
                time.sleep(1 / self.leak_rate)
            else:
                # Nothing to process — sleep briefly rather than spinning at 100% CPU
                # 0.1s is short enough to feel responsive when new requests arrive
                time.sleep(0.1)

    def add_request(self, request_id: int) -> bool:
        with self.lock:
            if not self.queue.full():
                # Space available — enqueue the request to be processed later
                # e.g. queue has 3/5 slots used → put request_id in, return True
                self.queue.put(request_id)
                return True
            else:
                # Queue is at capacity — drop the request immediately
                # e.g. queue has 5/5 slots used → return False (caller knows it was rejected)
                return False

    def stop_processing(self):
        if self.processing:
            self.processing = False
            # Signal the background thread to exit its while loop on its next iteration
            self.stop_event.set()
            if hasattr(self, 'process_thread'):
                # Block until the thread finishes so we don't exit while it's mid-request
                self.process_thread.join()


'''
The fixed window counter algorithm:

    Time is divided into fixed windows (e.g., 1 second)
    Each window has a maximum request limit
    When a request arrives:
        If the current window's counter is below the limit, increment and allow
        If the counter is at the limit, reject the request
    At the start of each new window, the counter resets to zero
'''

class FixedWindowCounter:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        # Counter for how many requests have been allowed in the current window
        self.count = 0
        # Marks the start of the current window so we know when to reset
        self.window_start = time.time()
        self.lock = threading.Lock()

    def reset_window(self):
        now = time.time()
        # Check if we've moved past the current window boundary
        # e.g. window_size=1s, window_start=10.0, now=11.2 → elapsed=1.2 → reset
        if now - self.window_start >= self.window_size:
            # New window starts fresh — drop the old count entirely
            # Note: this means requests at the very end of window N and start of window N+1
            # can together exceed the limit (a known trade-off of fixed windows)
            self.count = 0
            self.window_start = time.time()

    def allow_request(self) -> bool:
        with self.lock:
            # Always reset first so the counter reflects the current window
            self.reset_window()

            if self.count < self.limit:
                # Still under the limit — allow and increment
                # e.g. limit=5, count=3 → count becomes 4, return True
                self.count += 1
                return True
            else:
                # Limit reached for this window — reject until the window resets
                # e.g. limit=5, count=5 → return False
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
        # Stores the exact timestamp of every allowed request
        # Memory grows with traffic — each request costs one timestamp entry
        self.request_log = []
        self.lock = threading.Lock()

    def clean_old_requests(self):
        now = time.time()
        # Drop any timestamps that fall outside the sliding window
        # e.g. window_size=1s, now=10.5 → keep timestamps > 9.5, discard the rest
        # This is what makes the window "slide" — the cutoff moves forward with time
        self.request_log = [timestamp for timestamp in self.request_log if now - timestamp < self.window_size]

    def allow_request(self) -> bool:
        with self.lock:
            # Purge stale entries before counting so the limit check is accurate
            self.clean_old_requests()

            if len(self.request_log) < self.limit:
                # Fewer requests in the window than the limit — record this one and allow
                # e.g. limit=5, log has 3 entries → append now, return True
                self.request_log.append(time.time())
                return True
            else:
                # Window is full — reject without logging (rejected requests don't count)
                # e.g. limit=5, log has 5 entries → return False
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
        # Tracks requests in the ongoing window
        self.current_window = 0
        # Tracks requests from the previous window — used for the weighted estimate
        self.previous_window = 0
        self.window_start = time.time()
        self.lock = threading.Lock()

    def _reset_window(self):
        """
        Advance window counters when a full window period has elapsed.
        This method is called before each request check.
        """
        now = time.time()
        if now - self.window_start >= self.window_size:
            # The current window is now the "old" window for weighting purposes
            # e.g. current_window=8 → previous_window=8, current_window resets to 0
            self.previous_window = self.current_window
            self.current_window = 0
            self.window_start = now

    def allow_request(self) -> bool:
        """
        Check if a new request is allowed using weighted counters.

        The weighted count estimates how many of the previous window's requests
        still fall inside the sliding window. For example:
            - window_size=1s, previous_window=10, 30% through current window
            - weighted = 10 * (1 - 0.3) = 7 requests still "counted" from before
            - total = 7 + current_window requests
        This avoids storing every timestamp (like SlidingWindowLog) while still
        approximating a true sliding window more accurately than FixedWindowCounter.

        Returns:
            bool: True if request is allowed, False if rate limit exceeded
        """
        with self.lock:
            self._reset_window()
            current_time = time.time()
            # How far into the current window are we? 0.0 = just started, 1.0 = almost over
            # e.g. window_size=1s, elapsed=0.3s → window_progress=0.3
            window_progress = (current_time - self.window_start) / self.window_size

            # Weight the previous window's count by how much of it is still within range
            # The further into the current window we are, the less the previous window counts
            # e.g. previous_window=10, window_progress=0.3 → weighted_count = 10 * 0.7 = 7
            weighted_count = self.previous_window * (1 - window_progress)
            total_count = weighted_count + self.current_window

            if total_count < self.max_requests:
                # Estimated total is under the limit — allow and increment current window
                self.current_window += 1
                return True
            # Estimated total meets or exceeds the limit — reject
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
