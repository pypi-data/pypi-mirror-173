class Foo:
    def __init__(self, name="foo", msg="hello"):
        self.name = name
        self.msg = msg

    def greet(self):
        print(f"{self.msg} from {self.name}")

