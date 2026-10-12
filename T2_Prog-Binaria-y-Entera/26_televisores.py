from docplex.mp.model import Model
import numpy as np

mdl = Model(name='Distribución de productos')

# ==== Variables de decision ====
productoras = ['P', 'B']
distribuidoras = ['V', 'D']

productoras_i = range(len(productoras))   # [0, 1, 2, 3, 4]
distribuidoras_j = range(len(distribuidoras)) # [0, 1, 2, 3, 4]

x = mdl.integer_var_matrix(productoras, distribuidoras, name='x')

# ==== Restricciones ====

# datos asociados a las productoras y distribuidoras
oferta = {
    'P': 200,   # Portland
    'B': 600    # Baltimore
}

demanda = {
    'V': 300,   # Las Vegas
    'D': 400    # Detroit
}

# oferta
mdl.add_constraints(
    mdl.sum(x[i, j] for j in distribuidoras) <= oferta[i]
    for i in productoras
)

# demanda
mdl.add_constraints(
    mdl.sum(x[i, j] for i in productoras) >= demanda[j]
    for j in distribuidoras
)

# ==== Funcion objetivo ====
# costos de transporte c[i, j]
costos = {
    ('P', 'V'): 30,
    ('P', 'D'): 40,
    ('B', 'V'): 60, 
    ('B', 'D'): 50  
}

# Funcion Objetivo
mdl.minimize(
    mdl.sum(costos[i, j] * x[i, j] for i in productoras for j in distribuidoras)
)

# Resolver e imprimir solucion
solution = mdl.solve(log_output=True,)


print(solution)