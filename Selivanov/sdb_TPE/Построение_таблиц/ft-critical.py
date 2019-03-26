from scipy.stats import t,f

x_vec = [i*0.0001 for i in range(int(5/0.0001))]

# ймовірність по варіанту
prob = 0.95
par = 0.5 + prob/0.1*0.05

for i in x_vec:
    # другий аргумент для t.cdf() - степінь свободи f3
    if abs(t.cdf(i,16)-par) < 0.000005:
        print("t_critical =", i)
        break

x_vec = [i*0.001 for i in range(int(10/0.001))]

# другий аргумент f4 = N - d, третій аргумент f3 = f1*f2 = (m-1)*N
d = 1 # по варіанту
for i in x_vec:
    if abs(f.cdf(i,4-d,16)-prob) < 0.0001:
        print("f_critical =", i)
        break

print("solved for probablility", prob)
