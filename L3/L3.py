from random import uniform
import numpy as np


XMIN, XMAX = [-5, -25, -5], [15, 10, 20]
YMAX, YMIN = 200 + np.mean(XMAX), 200 + np.mean(XMIN)
#Normirovanie x
N_MATRIX = [[1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1 , 1], [1, 1, 1, -1]]
N = 4
FISHER_8_005 = [5.3, 4.5, 4.1, 3.8]


m = 3
#Naturalizirovanie x
x = [[XMAX[j] if N_MATRIX[i][j + 1] > 0 else XMIN[j] for j in range(m)]
 for i in range(N)]
y = [[uniform(YMIN, YMAX) for j in range(m)] for i in range(N)]

y_mean = [np.mean(i) for i in y]
x_mean = [np.mean([j[i] for j in x]) for i in range(m)]
my = np.mean(y)

a = [np.mean([x[j][i] * y_mean[j] for j in range(N)]) for i in range(m)]
a_2d = [[np.mean([x[k][i] * x[k][j] for k in range(N)]) for j in range(m)]
        for i in range(m)]
#naturalizovani coef
b = np.linalg.solve(
    [[1, *x_mean], *[[x_mean[j], *[i[j] for i in a_2d]] for j in range(m)]], 
    [my, *a])

dx = [(XMAX[i] - XMIN[i]) / 2 for i in range(m)]
#normirovanii coef
b_norm = [my, *[b[i + 1] * dx[i] for i in range(m)]]

m = 3
dispersions = [np.var(i) for i in y]

#Kokhren check
gp = max(dispersions) / sum(dispersions)
f1 ,f2 = m - 1, N

#Student check
s_b = np.mean(dispersions)
s_quad_betta = (s_b / m / N)
s_betta = s_quad_betta ** .5
bettas = [np.mean([y_mean[j] * N_MATRIX[i][j] for j in range(N)])
 for i in range(N)]
t = [abs(i) / s_betta for i in bettas]
f3 = f1 * f2
#Uroven' znachimosti = .05
t_table = 2.306
new_b = [b[i] if t[i] > t_table else 0 for i in range(N)]
new_y = [new_b[0] + sum([new_b[j + 1] * x[i][j] for j in range(m)])
 for i in range(N)]

#Fisher's criterion
d = sum([bool(i) for i in new_b])
f4 = N - d
if f4:
    s_quad_ad = m / (N - d) * sum([(new_y[i] - y_mean[i]) ** 2
     for i in range(N)])
    fp = s_quad_ad / s_quad_betta

print('y = b0 + b1x1 + b2x2 + b3x3')
print('y = {:.3f} + {:.3f}*x1 + {:.3f}*x2 + {:.3f}*x3'.format(*b))
print(*['{:.3f} + {:.3f}*{:>2} + {:.3f}*{:>2} + {:.3f}*{:>2} = {:.3f}'.format(
    b[0], b[1], x[i][0], b[2], x[i][1], b[3], x[i][2], 
    b[0] + sum([b[j + 1] * x[i][j] for j in range(m)])
    ) for i in range(N)], sep='\n')
print('y = {:.3f} + {:.3f}*x1 + {:.3f}*x2 + {:.3f}*x3'.format(*b_norm))
print(*['{:.3f} + {:.3f}*{:>2} + {:.3f}*{:>2} + {:.3f}*{:>2} = {:.3f}'.format(
    b_norm[0], b_norm[1], N_MATRIX[i][1], b_norm[2], N_MATRIX[i][2], 
    b_norm[3], N_MATRIX[i][3], 
    b_norm[0] + sum([b_norm[j + 1] * N_MATRIX[i][j + 1] for j in range(m)])
    ) for i in range(N)], sep='\n')
print('Y average: {:.3f}, {:.3f}, {:.3f}, {:.3f}'.format(*y_mean))

print('Kokhren\'s check: ', gp < .7679)
print(''.join([' t{}>t_tabl ' if i else ' t{}<t_tabl '
 for i in new_b]).format(0, 1, 2, 3))
if f4:
    print('Fisher\'s criterion: ', fp < FISHER_8_005[f4 - 1])
else:
    print('All coefficients are significant')
