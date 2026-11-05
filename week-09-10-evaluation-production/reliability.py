"""Bounded retries for explicitly transient, idempotent operations."""

import time


def retry(operation, attempts: int = 3, base_delay: float = 0.1,
          sleep=time.sleep):
    if not 1 <= attempts <= 3 or base_delay < 0:
        raise ValueError("Use 1-3 attempts and a non-negative delay.")
    for attempt in range(attempts):
        try:
            return operation()
        except (TimeoutError, ConnectionError):
            if attempt == attempts - 1:
                raise
            sleep(base_delay * 2 ** attempt)
