import time
from functools import wraps

def timeit(func):
    """装饰器，用于计算和打印函数执行时间"""

    @wraps(func)  # 保留原始函数的元数据
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # 高精度计时开始
        result = func(*args, **kwargs)    # 执行原始函数
        tt = time.perf_counter() - start    # 高精度计时结束

        print(f"func {func.__name__}() executed in: {tt*1000:.3f}ms ({tt:.6f}s)")

        return result

    return wrapper


def timeit_with_logging(logger=None, level='info'):
    """带日志记录的时间测量装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            tt = time.perf_counter() - start

            message = f"func {func.__name__}() executed in: {tt*1000:.3f}ms ({tt:.6f}s)"

            if logger:
                getattr(logger, level)(message)
            else:
                print(message)

            return result

        return wrapper

    return decorator

if __name__ == "__main__":
    # 使用示例
    @timeit
    def example_function(n):
        """示例函数，计算0到n-1的和"""
        return sum(range(n))

    # 调用被装饰的函数
    example_function(1000000)
    # 使用示例
    @timeit_with_logging()
    def another_example():
        time.sleep(1)

    another_example()
