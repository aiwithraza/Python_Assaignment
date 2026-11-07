import functools
import time


def ttl_cache(seconds):
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds <= 0:
        raise ValueError("seconds must be a number greater than 0")

    def decorator(func):
        cache = {}
        stats = {"hits": 0, "misses": 0}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))

            try:
                hash(key)
            except TypeError:
                stats["misses"] += 1
                return func(*args, **kwargs)

            if key in cache:
                result, saved_at = cache[key]
                if time.monotonic() - saved_at < seconds:
                    stats["hits"] += 1
                    return result

            stats["misses"] += 1
            result = func(*args, **kwargs)
            cache[key] = (result, time.monotonic())
            return result

        def cache_info():
            return {"hits": stats["hits"], "misses": stats["misses"], "size": len(cache)}

        def cache_clear():
            cache.clear()
            stats["hits"] = 0
            stats["misses"] = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return decorator


def main():
    @ttl_cache(0.5)
    def add_numbers(x, y):
        """Adds two numbers."""
        print("   (really calculating...)")
        return x + y

    print("name kept:", add_numbers.__name__, "| doc:", add_numbers.__doc__)

    print("call 1 (x=2, y=3):", add_numbers(x=2, y=3), add_numbers.cache_info())
    print("call 2 (y=3, x=2):", add_numbers(y=3, x=2), add_numbers.cache_info())
    print("call 3 (list arg):", add_numbers([1], [2]), add_numbers.cache_info())

    time.sleep(0.6)
    print("call 4 after expiry:", add_numbers(x=2, y=3), add_numbers.cache_info())


if __name__ == "__main__":
    main()