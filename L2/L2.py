from random import randint
import numpy as np


X1MIN, X1MAX, X2MIN, X2MAX, YMIN, YMAX = -5, 15, -25, 10, -20, 80
X1, X2 = [-1, 1, -1], [-1, -1, 1]
RKR = [1.69, 1.73, 2, 2, 2, 2,16, 2,17, 2,43, 2,29, 2,62, 2.39, 2.75]


m = 4
while True:
    m += 1
    a = [[randint(YMIN, YMAX) for j in range(m)] for i in range(3)]
    y_av = [np.mean(i) for i in a]
    ds = [np.var(i) for i in a]
    o0 = (4 * (m - 1) / (m * (m - 4))) ** 0.5
    fs = list(map(lambda x, y: max(x / y, y / x), 
                [ds[0], ds[0], ds[1]], [ds[1], ds[2], ds[2]]))
    os = [(m - 2) / m * fs[i] for i in range(3)]
    rs = [abs(os[i] - 1) / o0 for i in range(3)]
    if sum([bool(rs[i] < RKR[m - 1]) for i in range(3)]) == 3:
        break
mx1, mx2 = np.mean(X1), np.mean(X2)
my = np.mean(y_av)
a1, a2, a3 = tuple(map(np.mean, 
    [[i ** 2 for i in X1], 
    [X1[i] * X2[i] for i in range(3)], 
    [i ** 2 for i in X2]]))
a11 = np.mean([X1[i] * y_av[i] for i in range(3)])
a22 = np.mean([X2[i] * y_av[i] for i in range(3)])
b = np.linalg.solve([[1, mx1, mx2], [mx1, a1, a2], [mx2, a2, a3]], 
                    [my, a11, a22])
dx1, dx2 = (X1MAX - X1MIN) / 2, (X2MAX - X2MIN) / 2
x10, x20 = (X1MAX + X1MIN) / 2, (X2MAX + X2MIN) / 2
nat_a = [b[0] - b[1] * x10 / dx1 - b[2] * x20 / dx2, b[1] / dx1, b[2] / dx2]

template = ' '.join(['{:>8}'] * 3) + ' '.join(['{:>8.1f}'] * 5)
templatez = ' '.join(['{:>8}'] * 8)
array = [[i + 1] + [X1[i]] + [X2[i]] + a[i] for i in range(3)]
t = [(X1MAX if X1[i] > 0 else X1MIN, X2MAX if X2[i] > 0 else X2MIN) for i in range(3)]
print('y=b0 + b1x1 + b2x2\n')
print(templatez.format(*['', 'x1', 'x2', 'y1', 'y2', 'y3', 'y4',' y5']))
print(*[template.format(*array[i]) for i in range(3)], sep='\n')
print('Нормоване\n{:.3f} + {:.3f}*x1 + {:.3f}*x2'.format(*b))
print(*['{:.3f} + {:.3f}*{:>2} + {:.3f}*{:>2} = {:.1f}'.format(
    b[0], b[1], X1[i], b[2], X2[i], b[0]+b[1]*X1[i]+b[2]*X2[i]
    ) for i in range(3)], sep='\n')
print('Натуралізоване\n{:.3f} + {:.3f}*x1 + {:.3f}*x2'.format(*nat_a))
print(*['{:.3f} + {:.3f}*{:>2} + {:.3f}*{:>2} = {:.1f}'.format(
    nat_a[0], nat_a[1], t[i][0], nat_a[2], t[i][1], nat_a[0]+nat_a[1]*t[i][0]+nat_a[2]*t[i][1]
    ) for i in range(3)], sep='\n')