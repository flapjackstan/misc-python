from functools import wraps
 
def a_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("wrapper start")
        func(*args, **kwargs)
        print("wrapper end")
    return wrapper
 
@a_decorator
def first_function():
    print("first function")
 
@a_decorator
def second_function(a):
    print(a)

def main():
    first_function()
    second_function("test")

if __name__ == '__main__':
    main()