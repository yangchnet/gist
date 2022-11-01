# 实现数据模型的类型约束


class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Typed(Descriptor):
    """
    Typed 检查value是否是expected_type类型
    """
    expected_type = type(None)  # 这个属性将被子类覆盖

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"expected {self.expected_type}")
        super().__set__(instance, value)


class Unsigned(Descriptor):
    """
    Unsigned 检查给定value是否>=0
    """

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        super().__set__(instance, value)


class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size options')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError(f'size must be < {self.size!s}')


class Integer(Typed):
    expected_type = int


class UnsignedInteger(Integer, Unsigned):
    pass


class Float(Typed):
    expected_type = float


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed):
    expected_type = str


class SizedString(String, MaxSized):
    pass


class Stock:
    name = SizedString('name', size=8)
    age = Integer(18)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')

    def __init__(self, name, age, shares, price):
        self.name = name
        self.age = age
        self.shares = shares
        self.price = price


if __name__ == '__main__':
    s = Stock("stock", 1, 1, 1.0)
