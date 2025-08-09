class ImmutableMeta(type):
    """不可修改类成员类元类"""
    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            raise AttributeError(f"Cannot modify class variable: {name}")
        super().__setattr__(name, value)


class NoInstanceClass:
    """禁止实例化类"""
    def __init__(self):
        raise TypeError("Cannot instantiate this class")

class Singleton:
    """单例类"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance