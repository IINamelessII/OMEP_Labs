from functools import partial
from random import uniform
import numpy as np
from scipy.stats import f, t


def cohren(f1, f2, q=0.05):
    fisher_value = f.ppf(q=1-(q/f2), dfn=f1, dfd=(f2-1)*f1)
    return fisher_value / (fisher_value + f2 - 1)


def student(f3):
    return partial(t.ppf, q=1-0.025)(df=f3)


def fisher(f3, f4):
    return partial(f.ppf, q=1-0.05)(dfd=f3, dfn=f4)


def all_stuff(n):
    if n == 4:
        #Normirovanie x
        N_MATRIX = [[1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1 , 1], [1, 1, 1, -1]]
    elif n == 8:
        #Normirovanie x
        N_MATRIX = [[1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1 , 1], [1, 1, 1, -1]]
    
    m = 2
    while True:
        m += 1
        #Naturalizirovanie x
        x = [[XMAX[j] if N_MATRIX[i][j + 1] > 0 else XMIN[j] for j in range(3)]
        for i in range(n)]
        y = [[uniform(YMIN, YMAX) for j in range(m)] for i in range(n)]

        y_mean = [np.mean(i) for i in y]
        x_mean = [np.mean([j[i] for j in x]) for i in range(3)]
        my = np.mean(y)

        a = [np.mean([x[j][i] * y_mean[j] for j in range(n)]) for i in range(m)]
        a_2d = [[np.mean([x[k][i] * x[k][j] for k in range(n)]) for j in range(m)]
                for i in range(m)]
        #naturalizovani coef
        b = np.linalg.solve(
            [[1, *x_mean], *[[x_mean[j], *[i[j] for i in a_2d]] for j in range(m)]], 
            [my, *a])

        dx = [(XMAX[i] - XMIN[i]) / 2 for i in range(m)]
        #normirovanii coef
        b_norm = [my, *[b[i + 1] * dx[i] for i in range(m)]]

        # m = 3
        dispersions = [np.var(i) for i in y]

        #Kokhren check
        gp = max(dispersions) / sum(dispersions)
        f1 ,f2 = m - 1, n
        if gp < cohren(f1, f2):
            break

    #Student check
    s_b = np.mean(dispersions)
    s_quad_betta = (s_b / m / n)
    s_betta = s_quad_betta ** .5
    bettas = [np.mean([y_mean[j] * N_MATRIX[i][j] for j in range(n)])
    for i in range(n)]
    t = [abs(i) / s_betta for i in bettas]
    f3 = f1 * f2
    t_table = student(f3)
    # print(f3, t_table)
    new_b = [b[i] if t[i] > t_table else 0 for i in range(n)]
    new_y = [new_b[0] + sum([new_b[j + 1] * x[i][j] for j in range(m)])
    for i in range(n)]

    print('y = b0 + b1x1 + b2x2 + b3x3')
    print('y = {:.3f} + {:.3f}*x1 + {:.3f}*x2 + {:.3f}*x3'.format(*b))
    print(*['{:.3f} + {:.3f}*{:>2} + {:.3f}*{:>2} + {:.3f}*{:>2} = {:.3f}'.format(
        b[0], b[1], x[i][0], b[2], x[i][1], b[3], x[i][2], 
        b[0] + sum([b[j + 1] * x[i][j] for j in range(m)])
        ) for i in range(n)], sep='\n')
    print('y = {:.3f} + {:.3f}*x1 + {:.3f}*x2 + {:.3f}*x3'.format(*b_norm))
    print(*['{:.3f} + {:.3f}*{:>2} + {:.3f}*{:>2} + {:.3f}*{:>2} = {:.3f}'.format(
        b_norm[0], b_norm[1], N_MATRIX[i][1], b_norm[2], N_MATRIX[i][2], 
        b_norm[3], N_MATRIX[i][3], 
        b_norm[0] + sum([b_norm[j + 1] * N_MATRIX[i][j + 1] for j in range(m)])
        ) for i in range(n)], sep='\n')
    print('Y average: {:.3f}, {:.3f}, {:.3f}, {:.3f}'.format(*y_mean))
    print(''.join([' t{}>t_tabl ' if i else ' t{}<t_tabl '
    for i in new_b]).format(0, 1, 2, 3))

    #Fisher's criterion
    d = sum([bool(i) for i in new_b])
    f4 = n - d
    should_do_full = False
    if f4: #if f4 is not 0 (in that case will be division by zero)
        s_quad_ad = m / (N - d) * sum([(new_y[i] - y_mean[i]) ** 2
        for i in range(n)])
        fp = s_quad_ad / s_quad_betta
        if fp < fisher(f3, f4):
            print('Fisher\'s criterion: The equation is adequate to the model')
        else:
            should_do_full = True
            print('Fisher\'s criterion: The equation is not adequate to the model')
    else:
        print('All coefficients are significant')
    return should_do_full


XMIN, XMAX = [10, 10, 10], [40, 60, 15]
YMAX, YMIN = 200 + np.mean(XMAX), 200 + np.mean(XMIN)

if __name__ == "__main__":
    if all_stuff(n=4):
        print('\nWe carry out a full three-factor experiment:\n')
        all_stuff(n=8)
