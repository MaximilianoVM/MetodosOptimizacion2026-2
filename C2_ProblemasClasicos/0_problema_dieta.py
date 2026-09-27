from docplex.mp.model import Model


m = Model("Problema de la dieta")


# Parametros
c = [2,3.5,8,1.5,11,1]
b = [0,8,10,300]
a = [[4,8,7,1.3,8,9.2],
    [1,5,9,0.1,7,1],
    [15,11.7,0.4,22.6,0,17],
    [90,120,106,97,130,180]]


# Conjuntos
alimento = [(i) for i in range(6)] # pan,leche,queso,papa,pescado,yogurt
nutriente = [(j) for j in range(4)]


# Definir variables de decision
x = m.continuous_var_dict(alimento, name='x')


# Definir las restricciones
m.add_constraints(m.sum(a[j][i]*x[i] for i in alimento) >= b[j] for j in nutriente)

# proteina maxima
m.add_constraint(m.sum(a[0][i]*x[i] for i in alimento) <= 10)

# pescado minimo
m.add_constraint(x[4] >= 0.5)

# leche minimo
m.add_constraint(x[1] <= 1)


# Definir la funcion objetivo
m.minimize(m.sum(c[i]*x[i] for i in alimento))


# Resolver e imprimir solucion
solution = m.solve(log_output=True,)
print(solution)
m.export_as_lp(path=".")