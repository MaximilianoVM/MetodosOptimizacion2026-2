from docplex.mp.model import Model

d = [
    [5, 12, 20, 8, 15],
    [15, 6, 9, 20, 5],
    [8, 20, 5, 12, 18],
    [20, 15, 12, 5, 9],
]

S = 10
a = [[1 if d[i][j] <= S else 0 for j in range(5)] for i in range(4)]
f = [120, 80, 200, 150, 90]

mdl = Model(name='Facility Location P4')

n = 4  # ubicaciones candidatas
m = 5  # zonas demandantes
n_max = 2  # maximo de antenas a abrir

# y_i = se abre la antena i?
y = mdl.binary_var_list(n, name='y')
# x_j = queda cubierta la zona j?
x = mdl.binary_var_list(m, name='x')

# Restriccion de presupuesto
mdl.add_constraint(mdl.sum(y[i] for i in range(n)) <= n_max)

# Restriccion de cobertura
mdl.add_constraints(
    mdl.sum(a[i][j]*y[i] for i in range(n)) >= x[j] for j in range(m))

# Maximizar poblacion cubierta
mdl.maximize(
    mdl.sum(f[j]*x[j] for j in range(m))
    )


# Resolver e imprimir solucion
solution = mdl.solve(log_output=True,)


print(solution)