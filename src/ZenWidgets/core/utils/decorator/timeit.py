import time
from functools import wraps

def Timeit(logger=None, level='info', repeat=1):
    """
    时间测量装饰器，支持日志记录和重复执行功能

    :param logger: 日志记录器，为 None 时使用 print 输出
    :param level: 日志级别，默认为 'info'
    :param repeat: 重复执行次数，默认为 1
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            total_time = 0.0
            results = []

            # 处理重复执行逻辑
            if repeat > 1:
                print(f"preparing to run method {func.__name__} {repeat} times")

            for i in range(repeat):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                elapsed = end - start

                total_time += elapsed
                results.append(result)

                # 重复执行时的单次信息输出
                if repeat > 1 and (repeat <= 10 or i % (repeat // 10) == 0):
                    print(f"The {i+1}th run took {elapsed:.6f}s")

            # 计算时间信息
            if repeat == 1:
                tt = total_time
                message = f"func {func.__name__}() executed in: {tt*1000:.3f}ms ({tt:.6f}s)"
            else:
                avg_time = total_time / repeat
                message = (f"func {func.__name__}() repeated {repeat} times | "
                          f"total: {total_time:.6f}s | "
                          f"average: {avg_time:.6f}s")

            # 处理输出方式（日志或打印）
            if logger:
                getattr(logger, level)(message)
            else:
                print(message)

            # 返回结果（最后一次执行的结果）
            return results[-1] if results else None
        return wrapper
    return decorator


# 使用示例
if __name__ == "__main__":
    # 1. 基本计时功能（类似Timeit）
    @Timeit()
    def example1(n):
        return sum(range(n))
    example1(1000000)

    # 2. 带日志记录功能（类似timeit_with_logging）
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @Timeit(logger=logger, level='warning')
    def example2():
        time.sleep(0.5)
    example2()

    # 3. 重复执行功能（类似repeatit）
    @Timeit(repeat=5)
    def example3(n):
        return sum(i*i for i in range(n))
    result = example3(10000)
    print(f"最终结果: {result}")

    # 4. 同时使用日志和重复执行
    @Timeit(logger=logger, repeat=3)
    def example4():
        time.sleep(0.2)
    example4()