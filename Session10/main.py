from threading import Thread


def add():
    a = 5
    b = 6
    print(a + b)


def sub():
    a = 5
    b = 6
    print(a - b)


print(Thread(None, add).start()) #tao mot tread
print(sub())