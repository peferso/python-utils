def a_static_function():
    x = 'hello world'
    return x

class aClass():
    def __init__(self):
        pass
    def print_hello_world(self):
        print(a_static_function())

