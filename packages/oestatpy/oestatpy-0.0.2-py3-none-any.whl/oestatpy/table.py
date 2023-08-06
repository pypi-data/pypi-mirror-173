from fractions import Fraction
import numpy as np



def _get_row(row):
    return tuple(Fraction(col) for col in row.split())

def _get_table(table):
    return tuple(_get_row(row) for row in table.split('\n'))

def _calc(array, values, axis):
    probability_distribution = np.sum(array, axis=axis)
    expected_value = np.sum(values * probability_distribution)
    variance = np.sum(probability_distribution * (values-expected_value)**2)
    return probability_distribution, expected_value, variance


def calculate(_e, _n, _p):
    e = np.array(_get_row(_e))
    n = np.array(_get_row(_n))
    p = np.array(_get_table(_p))

    P = tuple(_calc(p, v, i) for i, v in enumerate((e, n)))

    cov = np.sum(p*e*n.reshape(-1, 1)) - P[0][1]*P[1][1]
    ro = cov / (P[0][2]*P[1][2]) ** 0.5

    for k in range(2):
        print(*P[k][0])
        print(*P[k][1:], sep='\n', end='\n\n')
    print(cov, ro, sep='\n')
