from abc import ABC, abstractmethod

'''
descriptor 就是任何一个定义了 __get__(), __set__() 或 __delete__() 的对象。

可选地，描述器可以具有 __set_name__() 方法。这仅在描述器需要知道创建它的类或分配给它的类变量名称时使用。（即使该类不是描述器，只要此方法存在就会调用。）

在属性查找期间，描述器由点运算符调用。如果使用 vars(some_class)[descriptor_name] 间接访问描述器，则返回描述器实例而不调用它。

描述器仅在用作类变量时起作用。放入实例时，它们将失效。

描述器的主要目的是提供一个挂钩，允许存储在类变量中的对象控制在属性查找期间发生的情况。
'''


class Validator(ABC):
    """既是一个 abstract base class 也是一个托管属性描述器。
    自定义验证器需要从 Validator 继承，并且必须提供 validate() 方法以根据需要测试各种约束
    """

    def __set_name__(self, owner, name):
        """在Validator被创建时调用

        Args:
            owner (objects): 描述器在哪个类中被调用
            name (str): 描述器实例的名字
        """
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        """当Validator实例被调用时执行

        Args:
            instance (objects): 描述器的调用实例
            owner (objects):
        """
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        """描述器实例被赋值时执行

        Args:
            instance (objects): 描述器的调用实例
            value (_type_): 描述器实例被赋予的值
        """
        self.validate(value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    '''
    验证一个值是否在给定的一组值内
    '''

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(
                f'Expected {value!r} to be one of {self.options!r}')


class Number(Validator):
    '''
    验证值是否为 int 或 float。根据可选参数，它还可以验证值在给定的最小值或最大值之间。
    '''

    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )


class String(Validator):
    '''
    验证值是否为 str。根据可选参数, 它可以验证给定的最小或最大长度。它还可以验证用户定义的 predicate。
    '''

    def __init__(self, minsize=None, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(
                f'Expected {self.predicate} to be true for {value!r}'
            )


class Component:

    name = String(minsize=3, maxsize=10, predicate=str.isupper)
    kind = OneOf('wood', 'metal', 'plastic')
    quantity = Number(minvalue=0)

    def __init__(self, name, kind, quantity):
        self.name = name
        self.kind = kind
        self.quantity = quantity
