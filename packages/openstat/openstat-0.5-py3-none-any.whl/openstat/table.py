from fractions import Fraction
import numpy as np



def _get_row(row):
    return tuple(Fraction(col) for col in row.split())

def _get_table(table):
    return tuple(_get_row(row) for row in table.split('\n'))

def _calc(array, values, axis):
    P = np.sum(array, axis=axis)
    E = np.sum(values * P)
    D = np.sum(P * (values-E)**2)
    return P, E, D


def calc(_e, _n, _p):
    e = np.array(_get_row(_e))
    n = np.array(_get_row(_n))
    p = np.array(_get_table(_p))

    Pe, Ee, De = _calc(p, e, 0)
    Pn, En, Dn = _calc(p, n, 1)

    cov = np.sum(p*e*n.reshape(-1, 1)) - Ee*En
    ro = cov / (De*Dn) ** 0.5

    return f'{Ee} {De}\n{En} {Dn}\n{cov} {ro}'
