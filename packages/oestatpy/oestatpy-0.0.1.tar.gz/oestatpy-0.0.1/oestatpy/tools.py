import math



def C(n, k):
    assert n >= k
    return math.factorial(n)//math.factorial(k)//math.factorial(n-k)

def B(n, p, f, t=0):
    t = t or f
    q = 1 - p
    return float(sum(C(n, i) * p**i * q**(n-i) for i in range(f, t+1)))

def P(n, p, f, t=0):
    t = t or f
    l = n * p
    s = sum(l**i / math.factorial(i) for i in range(f, t+1))
    return float(s / Fraction(math.e)**l)

def L(n, p, f, t=0, d=1000):
    t = t or f
    q = 1 - p
    result = 0
    t -= d > 1
    for i in range(f, t+1):
        for j in range(d):
            x = (i+j/d - n*p) / math.sqrt(n*p*q)
            result += math.exp(-(x**2) / 2) / d
    return result / math.sqrt(n*p*q*2*math.pi)

def Pe(n, p):
    return float(min(p, n*p**2))

def Le(n, p):
    return float(1 / (p*(1-p)*math.sqrt(n)))


def Gd(p, f, t=0):
    assert f > 0
    t = t or f
    q = 1 - p
    return sum(p*q**(i-1) for i in range(f, t+1))

def Pd(l, f, t=0):
    return P(l, 1, f, t)

def Ec(l, p):
    return 1 - math.exp(-l*p)
