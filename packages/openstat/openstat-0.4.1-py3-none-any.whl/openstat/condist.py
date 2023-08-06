import sympy as sp



def E(x, f, l, r):
    return sp.integrate(x*f, ('x', l, r))

def D(x, f, l, r):
    return E(x**2, f, l, r) - E(x, f, l, r)**2

def P(f, l, r):
    return lambda a, b: float(sp.integrate(f, ('x', max(l, a), min(r, b))))

def calc(f, l, r):
    f = sp.sympify(f)

    c, = sp.solve(sp.integrate(f, ('x', l, r))-1)
    f = f.subs('c', c)
    x, = f.free_symbols

    return P(f, l, r), f'{c} {E(x, f, l, r)} {D(x, f, l, r)}'
