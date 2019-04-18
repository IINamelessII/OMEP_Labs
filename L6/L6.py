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
    
    def print_equalations(b, x, add=0):
        print(
            *[('{:.3f} + ' + ' + '.join(['{:.3f}*{:>2}' for i in range(n - 1)]) + ' = {:.3f}').format(
            b[0], *[b[j // 2 + 1] if not j % 2 else x[i][j // 2 + add] for j in range((n - 1) * 2)],
             b[0] + sum([b[j + 1] * x[i][j + add] for j in range(n - 1)])) for i in range(N)],
        sep='\n')

    if n == 4:
        N = 4
        #Normirovanie x
        n_matrix = [
            [1, -1, -1, -1], 
            [1, -1, 1, 1], 
            [1, 1, -1 , 1], 
            [1, 1, 1, -1]
        ]
    elif n == 8:
        N = 8
        #Normirovanie x
        n_matrix = [
            [1, -1, -1, -1, 1, 1, 1, -1], 
            [1, -1, 1, 1, -1, -1, 1, -1],
            [1, 1, -1 , 1, -1, 1, -1, -1], 
            [1, 1, 1, -1, 1, -1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, -1, -1, -1, -1, 1, 1],
            [1, -1, 1, -1, -1, 1, -1, 1],
            [1, -1, -1, 1, 1, -1, -1, 1]
        ]
    elif n == 11:
        N = 15
        #Normirovanie x
        n_matrix = [
            [1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1], 
            [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1],
            [1, 1, -1 , 1, -1, 1, -1, -1, 1, 1, 1], 
            [1, 1, 1, -1, 1, -1, -1, -1, 1, 1 ,1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1],
            [1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1],
            [1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1],
            [1, -1.215, 0, 0, 0, 0, 0, 0, 1.47623, 0, 0],
            [1, 1.215, 0, 0, 0, 0, 0, 0, 1.47623, 0, 0],
            [1, 0, -1.215, 0, 0, 0, 0, 0, 0, 1.47623, 0],
            [1, 0, 1.215, 0, 0, 0, 0, 0, 0, 1.47623, 0],
            [1, 0, 0, -1.215, 0, 0, 0, 0, 0, 0, 1.47623],
            [1, 0, 0, 1.215, 0, 0, 0, 0, 0, 0, 1.47623],
            [1,0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    #Naturalizirovanie x
    if n == 4 or n == 8:
        x = [[
            n_matrix[i][j + 1] * abs(XMAX[j] if n_matrix[i][j + 1] > 0 else XMIN[j])
            for j in range(n - 1)]
            for i in range(N)]
    elif n == 11:
        x = [[
            n_matrix[i][j + 1] * abs(XMAX[j] if n_matrix[i][j + 1] > 0 else XMIN[j])
            for j in range(n - 1)]
            for i in range(8)]
        x += [[(n_matrix[i][j+1] * (XMAX[j] - (XMAX[j] + XMIN[j]) / 2)
                + (XMAX[j] + XMIN[j]) / 2)
              ** (j // 7 + 1) for j in range(10)] for i in range(7)]
    x_mean = [np.mean([j[i] for j in x]) for i in range(n - 1)]
    
    m = 2
    while True:
        m += 1
        
        y = [[uniform(YMIN, YMAX) for j in range(m)] for i in range(N)]
        y_mean = [np.mean(i) for i in y]
        my = np.mean(y)

        a = [np.mean([x[j][i] * y_mean[j] for j in range(N)]) for i in range(n - 1)]
        a_2d = [[np.mean([x[k][i] * x[k][j] for k in range(N)]) for j in range(n - 1)]
                for i in range(n - 1)]
        #naturalizovani coef
        b = np.linalg.solve(
            [[1, *x_mean], *[[x_mean[j], *[i[j] for i in a_2d]] for j in range(n - 1)]], 
            [my, *a])

        if n == 4:
            dx = [(XMAX[i] - XMIN[i]) / 2 for i in range(3)]
            #normirovanii coef
            b_norm = [my, *[b[i + 1] * dx[i] for i in range(3)]]
        elif n == 8:
            b_norm = [np.mean([y_mean[j] * n_matrix[j][i] for j in range(n)])
             for i in range(n)]
        
        dispersions = [np.var(i) for i in y]

        #Kokhren check
        gp = max(dispersions) / sum(dispersions)
        f1, f2 = m - 1, N
        if gp < cohren(f1, f2):
            break

    #Student check
    s_b = np.mean(dispersions)
    s_quad_betta = (s_b / m / N)
    s_betta = s_quad_betta ** .5
    bettas = [np.mean([y_mean[j] * n_matrix[i][j] for j in range(n)])
    for i in range(N)]
    t = [abs(i) / s_betta for i in bettas]
    f3 = f1 * f2
    t_table = student(f3)
    new_b = [b[i] if t[i] > t_table else 0 for i in range(n)]
    new_y = [new_b[0] + sum([new_b[j + 1] * x[i][j] for j in range(n - 1)])
    for i in range(N)]

    if n == 8:
        print('WARNING: b4 -> b12, b5 -> b13, b6 -> b23, b7 -> b123')
        print('WARNING: x4 -> x12, x5 -> x13, x6 -> x23, x7 -> x123')
    elif n == 11:
        print('WARNING: b4 -> b12, b5 -> b13, b6 -> b23, b7 -> b123, b8 -> b1^2, b9 -> b2^2, b10 -> b3^2')
        print('WARNING: x4 -> x12, x5 -> x13, x6 -> x23, x7 -> x123, x8 -> x1^2, x9 -> x2^2, x10 -> x3^2')
        
    print('y = b0 + ' + ' + '.join(['b{}x{}'.format(i + 1, i + 1) for i in range(n - 1)]))
    y_template = 'y = {:.3f} + ' + ' + '.join(['{:.3f}*x' + str(i + 1) for i in range(n - 1)])
    print(y_template.format(*b))
    print_equalations(b, x)
    if n == 4 or n == 8:
        print(y_template.format(*b_norm))
        print_equalations(b_norm, n_matrix, add=1)
    print('Y average: ' + ', '.join(['{:.3f}' for i in range(N)]).format(*y_mean))
    corrected_y_template = 'y = {:.3f} + ' + ' + '.join([('{:.3f}*x' if new_b[i + 1] else '')
     + str(i + 1) for i in range(n - 1)])
    print('Equation after correction:')
    print(corrected_y_template.format(*list(filter(None, new_b))))

    #Fisher's criterion
    d = sum([bool(i) for i in new_b])
    f4 = N - d
    should_do_more = False
    if f4: #if f4 is not 0 (in that case will be division by zero)
        s_quad_ad = m / f4 * sum([(new_y[i] - y_mean[i]) ** 2
        for i in range(N)])
        fp = s_quad_ad / s_quad_betta
        if fp < fisher(f3, f4):
            print('Fisher\'s criterion: The equation is adequate to the model')
        else:
            should_do_more = True
            print('Fisher\'s criterion: The equation is not adequate to the model')
    else:
        print('All coefficients are significant, we should increase N to N > k')
    return should_do_more


XMIN = [-2, 0, -4]
XMIN += [i * j for i in XMIN for j in XMIN if i < j] + [XMIN[0] * XMIN[1] * XMIN[2]]
XMIN += [i ** 2 for i in XMIN[:3]]
XMAX = [3, 10, 8]
XMAX += [i * j for i in XMAX for j in XMAX if i < j] + [XMAX[0] * XMAX[1] * XMAX[2]]
XMAX += [i ** 2 for i in XMAX[:3]]
YMAX, YMIN = 200 + np.mean(XMAX[:3]), 200 + np.mean(XMIN[:3])

if __name__ == "__main__":
    all_stuff(n=11)
