import time
import threading

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
        allowed = False
        with self.lock:
            if self.tokens >= tokens:
                self.tokens -= tokens
                allowed = True
            else:
                allowed = False
            self.refill()
            return allowed