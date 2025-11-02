class SingletonMeta(type):
    """单例元类"""
    # 元类的 __init__ 方法：在类（而非实例）创建时调用
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        # 给类绑定一个 __instance__ 属性，用于缓存单例
        cls.__instance__ = None

    # 元类的 __call__ 方法：在“类名()”创建实例时调用
    def __call__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            # 调用原类的 __init__ 创建实例（等价于 cls.__new__(cls, *args, **kwargs) + cls.__init__(...)）
            cls.__instance__ = super().__call__(*args, **kwargs)
        return cls.__instance__


# # 使用元类：通过 metaclass=SingletonMeta 指定类的元类
# class MyClass(metaclass=SingletonMeta):
#     """这是类的文档注解"""
#     class_var = 10

#     @classmethod
#     def class_method(cls):
#         return f"类方法调用，class_var={cls.class_var}"

#     def __init__(self, x=0):
#         self.x = x
