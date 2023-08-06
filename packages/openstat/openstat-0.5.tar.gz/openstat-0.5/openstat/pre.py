import re



vals = (
    {
        'G': lambda p: 1/p,
        'P': lambda l: l,
        'U': lambda a, b: (a+b)/2,
        'E': lambda l: 1/l,
        'N': lambda a, o2: a,
        'C': lambda c: c,
        'M': 1
    },
    {
        'G': lambda p: (1-p)/p**2,
        'P': lambda l: l,
        'U': lambda a, b: (b-a)**2/12,
        'E': lambda l: 1/l**2,
        'N': lambda a, o2: o2,
        'C': lambda c: 0,
        'M': 2
    }
)
steps = (
    ("(?=[A-Z])", "L['"),
    ("(?<='.)", "']("),
    ("(?<=\d)((?=[+-])|$)", ")"),
    ("(^|(?<=[+-]))(?=L)", "1"),
    ("^|(?=[+-])", "+("),
    ("(?<=\d)(?=L)", ")**L['M']*"),
)

def find(expr):
    result = []
    for L in vals:
        e = expr
        for p, r in steps:
            e = re.sub(p, r, e)
            print(e)
        result.append(eval(e))
    return result
