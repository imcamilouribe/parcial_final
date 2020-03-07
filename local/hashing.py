import random


def hasheo():
    x = 'T000'

    for i in range (5):
        x = x + str(random.randint(0,9))
    y = hash(x)
    return (y)



