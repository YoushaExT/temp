def outer(a, b):
    def inner():
        return a+b
    return inner()

print(outer(5,2))

class Person():
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name):
        super().__init__(name)


a = Person('ahmed')
b = Student('ali')
print(a.name, b.name)
print(a.name, isinstance(a, Person), isinstance(a, Student))
print(b.name, isinstance(b, Person), isinstance(b, Student))