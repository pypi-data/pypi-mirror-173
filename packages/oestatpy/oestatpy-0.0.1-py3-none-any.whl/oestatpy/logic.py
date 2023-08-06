def AND(a, b, *c):
    if c: b = AND(b, *c)
    return a*b

def OR(a, b, *c):
    if c: b = OR(b, *c)
    return a+b-AND(a, b)
