from random import random


def func(arr):
    return sum([a[i] * ([1,] + arr)[i] for i in range(4)])


BOUND = 20


#First task
x = [[random() * BOUND for j in range(3)]for i in range(8)] #8*3
#Second task
a = [random() for i in range(4)] #4
y = [func(x[i]) for i in range(8)] #8
#Third task
x0 = [(
    max([x[j][i] for j in range(8)]) + min([x[j][i] for j in range(8)])
) / 2 for i in range(3)] # 3
dx = [x0[i] - min([x[j][i] for j in range(8)]) for i in range(3)] #3
xn = [[(x[i][j] - x0[j]) / dx[j] for j in range(3)] for i in range(8)] #8*3
y_etalon = func(x0) #value
#Fourth task
index = 7
# while sorted(y)[index] > y_etalon:
#     index -= 1
# result = sorted(y)[index]
# result_index = y.index(sorted(y)[index])
while sorted(y)[index] > y_etalon:
    index -= 1
result = sorted(y)[index]
result_index = y.index(sorted(y)[index])

print('Y = {:.5f} + {:.5f} * X1 + {:.5f} * X2 + {:.5f} * X3\n'.format(*a))
sz = ['#', 'X1', 'X2', 'X3', 'Y', 'Xn1', 'Xn2', 'Xn3']
s = [[i + 1, x[i][0], x[i][1], x[i][2], y[i], xn[i][0], xn[i][1], xn[i][2]]
 for i in range(8)]
templatez = ' '.join(['{:>8}'] * 8)
template = '{:>8} ' + ' '.join(['{:>8.5f}'] * 7)
print(templatez.format(*sz))
print(*[template.format(*s[i]) for i in range(8)], sep='\n')
print('Y({:.5f}, {:.5f}, {:.5f}) = {:.5f}'.format(*x[result_index], result))
