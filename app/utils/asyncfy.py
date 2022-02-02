import asyncio
from functools import wraps


def asyncfy(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, func, *args, **kwargs)
    return wrapped
