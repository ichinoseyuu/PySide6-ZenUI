import time
from functools import wraps

def method_timer(times=1):
    """
    方法性能测试装饰器：运行函数指定次数并打印总时间
    参数:
        times (int): 需要运行的次数, 默认为1次
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            total_time = 0.0
            results = []

            print(f"准备运行 {func.__name__} {times} 次...")

            for i in range(times):
                start_time = time.perf_counter()  # 高精度计时
                result = func(*args, **kwargs)
                end_time = time.perf_counter()

                elapsed = end_time - start_time
                total_time += elapsed

                if times <= 10 or i % (times // 10) == 0:  # 对于大量运行时不每次都打印
                    print(f"第 {i+1} 次运行耗时: {elapsed:.6f} 秒")

                results.append(result)

            avg_time = total_time / times if times > 0 else 0
            print(f"\n{func.__name__} 运行结果:")
            print(f"总运行次数: {times}")
            print(f"总耗时: {total_time:.6f} 秒")
            print(f"平均每次耗时: {avg_time:.6f} 秒")

            # 如果函数有返回值，返回最后一次的结果
            return results[-1] if results else None

        return wrapper
    return decorator


# 使用示例
if __name__ == "__main__":
    @method_timer(times=5)
    def example_function(n):
        """示例函数:计算0到n的平方和"""
        return sum(i*i for i in range(n))

    result = example_function(10000)
    print(f"最终结果: {result}")
