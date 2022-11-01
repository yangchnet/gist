from abc import ABC, abstractmethod

strategy_dict = {}


def register(source_cls):
    strategy_dict[source_cls.name] = source_cls
    return source_cls


class BaseAddStrategy(ABC):
    @abstractmethod
    def add(self, a, b):
        pass


@register
class StringAddStrategy(BaseAddStrategy):
    name = "StringStrategy"

    def add(self, a: str, b: str) -> str:
        if not isinstance(a, str):
            raise TypeError(f"Expect {a!r} as str")
        if not isinstance(b, str):
            raise TypeError(f"Expect {b!r} as str")

        return a + ", " + b


@register
class IntegerAddStrategy(BaseAddStrategy):
    name = "IntegerStrategy"

    def add(self, a: int, b: int) -> int:
        if not isinstance(a, int):
            raise TypeError(f"Expect {a!r} as int")
        if not isinstance(b, int):
            raise TypeError(f"Expect {b!r} as int")

        return a+b


class Adder:
    def __init__(self, strategy: str):
        self.strategy = strategy_dict[strategy]()

    def add(self, a, b):
        print(f"adder start add, and use {self.strategy.name}: ", end='')
        print(self.strategy.add(a, b))


if __name__ == '__main__':
    a_str = Adder("StringStrategy")
    a_str.add("one", "two")
    print(a_str.__dict__)
    setattr()
    # a_str.add(1, 2)

    # a_int = Adder("IntegerStrategy")
    # a_int.add(23, 44)
    # a_int.add("one", "two")

