def outer(a, b):
    def inner():
        return a+b
    return inner()

print(outer(5,2))