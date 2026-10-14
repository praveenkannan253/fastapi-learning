def my_decorator(func):
    def wrapper():
        print("Preparing the pizza base..")
        func()
        print("Adding extra toppings before serving!")

    return wrapper


@my_decorator
def say_hello():
    print("Plain pizza is ready!")


say_hello()
