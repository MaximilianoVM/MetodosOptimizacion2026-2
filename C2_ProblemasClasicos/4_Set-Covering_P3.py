from docplex.mp.model import Model


municipios = [
	[1, 1, 0, 0, 0, 0], 
	[1, 1, 0, 0, 0, 1], 
	[0, 0, 1, 1, 0, 0],
	[0, 0, 1, 1, 1, 0], 
	[0, 0, 0, 1, 1, 1], 
	[0, 1, 0, 0, 1, 1]
]

mdl = Model(name='Set Covering P3')

# 6 municipios
n = 6
# x_i = se construye en i? 
x = mdl.binary_var_list(n, name='x')

# Restricciones
mdl.add_constraints(
    mdl.sum(municipios[i][j]*x[i] for i in range(n)) >= 1 for j in range(n))
    
# Minimizar el numero de estaciones
mdl.minimize(
    mdl.sum(x[i] for i in range(n))
    )


# Resolver e imprimir solucion
solution = mdl.solve(log_output=True,)


print(solution)