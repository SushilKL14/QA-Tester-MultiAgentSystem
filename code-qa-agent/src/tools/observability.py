# src/tools/observability.py
import logging
from time import time

logger = logging.getLogger("code_qa_agent")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s:%(message)s"))
logger.addHandler(ch)

# Simple metrics object for demo. In production integrate Prometheus / OpenTelemetry.
metrics = {
    "tests_generated": 0,
    "tests_run": 0,
    "tests_passed": 0,
    "tests_failed": 0,
}

def timeit(func):
    """Decorator to log execution time for observability."""
    def wrapper(*args, **kwargs):
        t0 = time()
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} took {time() - t0:.3f}s")
        return result
    return wrapper
