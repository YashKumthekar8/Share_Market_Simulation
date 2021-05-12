from cyberbrain import trace

@trace
def function():
    a = int(input('Enter the no: '))
    b = int(input('Enter the no: '))
    return (a+b)


print(function())