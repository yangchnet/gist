class A:
    def __init__(self):
        print("aaaa")


class B(A):
    def __init__(self):
        super().__init__()
        print('bbb')


b = B()
