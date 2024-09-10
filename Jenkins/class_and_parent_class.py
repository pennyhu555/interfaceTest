class Leaf:
    def hello(self):
        print(f"我叫{self.name}")


class Root(Leaf):
    def __init__(self):
        self.name = '老根'


if __name__ == "__main__":
    root = Root()
    root.hello()
    print("=====================")
    leaf = Leaf()
    leaf.hello()