import inspect
import os
import time
def advancedPrint(*args, **kwargs):
    """打印调试信息，包括文件名和行号"""
    # 获取调用栈信息
    caller = inspect.currentframe().f_back
    #filename = os.path.basename(caller.f_code.co_filename)
    filepath = caller.f_code.co_filename
    line_no = caller.f_lineno
    # 构造输出信息
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]:[{filepath}:{line_no}]\n", *args, **kwargs)