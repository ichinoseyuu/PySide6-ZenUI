class NonInstantiableMeta(type):
    """不可实例化的元类，禁止创建类的实例"""
    def __call__(cls, *args, **kwargs):
        """重写__call__方法，阻止实例化"""
        raise TypeError(f"类 {cls.__name__} 不可实例化")


# # 示例使用
# class MyClass(metaclass=NonInstantiableMeta):
#     """这是一个不可实例化的类的文档注解"""

#     # 类变量
#     class_var = "类变量值"

#     # 类方法
#     @classmethod
#     def class_method(cls):
#         return f"类方法调用，class_var={cls.class_var}"

#     # 静态方法
#     @staticmethod
#     def static_method():
#         return "这是静态方法"