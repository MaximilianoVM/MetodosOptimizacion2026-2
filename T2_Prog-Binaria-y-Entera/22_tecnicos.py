from docplex.mp.model import Model
import numpy as np

mdl = Model(name='Asignacion de tecnicos a trabajos')

# Tabla 1
tiempos = [
    # Tr1  Tr2  Tr3   Tr4   Tr5
    [45,   22,  30,   65,   15],  # Tec1
    [180,  163, 85,   148,  68],  # Tec2
    [21,   17,  193,  59,   65],  # Tec3
    [18,   83,  16,   70,   115], # Tec4
    [97,   75,  20,   70,   71],  # Tec5
]

tiempos_np = np.array(tiempos)

# tecnicos y trabajos
num_tecnicos = tiempos_np.shape[0]  # 5 filas
num_trabajos = tiempos_np.shape[1] # 5 columnas

tecnicos_i = range(num_tecnicos)   # [0, 1, 2, 3, 4]
trabajos_j = range(num_trabajos) # [0, 1, 2, 3, 4]

x = mdl.binary_var_matrix(tecnicos_i, trabajos_j, name='x')

# restricciones: cada tecnico i atiende exactamente un trabajo j
mdl.add_constraints(
    mdl.sum(x[i,j] for i in tecnicos_i) == 1 for j in trabajos_j
    )
    
# restricciones: cada trabajo j es atendido por exactamente un técnico i
mdl.add_constraints(
    mdl.sum(x[i,j] for j in trabajos_j) == 1 for i in tecnicos_i
    )
    
mdl.minimize(
    mdl.sum(tiempos_np[i,j] * x[i,j] for i in tecnicos_i for j in trabajos_j)
    )


# Resolver e imprimir solucion
solution = mdl.solve(log_output=True,)


print(solution)