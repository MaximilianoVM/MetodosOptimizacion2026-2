from docplex.mp.model import Model
import numpy as np

mdl = Model(name='Asignacion de ordenes a maquinas')

# Tabla 1
costos = [
    # M1  M2  M3   M4    M5
    [16,   4,  9,   5,   6],  # A1
    [2,   14,  7,   5,  13],  # A2
    [8,   10,  3,  12,  11],  # A3
    [3,    7,  6,  10,   5],  # A4
    [3,    6,  8,  11,   7],  # A5
]

costos_np = np.array(costos)

# ordenes y maquinas
num_ordenes = costos_np.shape[0]  # 5 filas
num_maquinas = costos_np.shape[1] # 5 columnas

ordenes_i = range(num_ordenes)   # [0, 1, 2, 3, 4]
maquinas_j = range(num_maquinas) # [0, 1, 2, 3, 4]

x = mdl.binary_var_matrix(ordenes_i, maquinas_j, name='x')

# restricciones: cada maquina puede procesar a lo sumo una orden
mdl.add_constraints(
    mdl.sum(x[i,j] for i in ordenes_i) == 1 for j in maquinas_j
    )
    
# restricciones: cada orden debe ser atendida
mdl.add_constraints(
    mdl.sum(x[i,j] for j in maquinas_j) == 1 for i in ordenes_i
    )
    
mdl.minimize(
    mdl.sum(costos_np[i,j] * x[i,j] for i in ordenes_i for j in maquinas_j)
    )


# Resolver e imprimir solucion
solution = mdl.solve(log_output=True,)


print(solution)