from docplex.mp.model import Model
import numpy as np

mdl = Model(name='Planeacion de encuestas')

# Tabla 7: Costos por tipo de hogar y horario
# Filas: Con mascotas (0), Sin mascotas (1)
# Columnas: Mañana (0), Tarde (1)
costos = [
    # M   T
    [20, 25],  # Con mascotas
    [18, 20],  # Sin mascotas
]

costos_np = np.array(costos)

# Indices
num_tipos = costos_np.shape[0]     # 2 filas (Con, Sin)
num_horarios = costos_np.shape[1]  # 2 columnas (Mañana, Tarde)

tipos_i = range(num_tipos)       # 0: Con mascotas, 1: Sin mascotas
horarios_j = range(num_horarios) # 0: Mañana, 1: Tarde

x = mdl.integer_var_matrix(tipos_i, horarios_j, lb=0, name='x')

# Restriccion 1: el cliente ha contratado 1,000 encuestas
mdl.add_constraint(
    mdl.sum(x[i,j] for i in tipos_i for j in horarios_j) == 1000
)

# Restriccion 2: al menos 400 hogares de cada tipo (con/sin mascotas)
mdl.add_constraints(
    mdl.sum(x[i,j] for j in horarios_j) >= 400 for i in tipos_i
)

# Restriccion 3: total tarde (j=1) >= total mañana (j=0)
mdl.add_constraint(
    mdl.sum(x[i,1] for i in tipos_i) >= mdl.sum(x[i,0] for i in tipos_i)
)

# Restriccion 4: al menos 40% de encuestas con mascotas (i=0) por la mañana (j=0)
mdl.add_constraint(
    x[0,0] >= 0.4 * mdl.sum(x[0,j] for j in horarios_j)
)

# Restriccion 5: al menos 60% de encuestas con mascotas (i=0) por la tarde (j=1)
mdl.add_constraint(
    x[0,1] >= 0.6 * mdl.sum(x[0,j] for j in horarios_j)
)

# Funcion objetivo
mdl.minimize(
    mdl.sum(costos_np[i,j] * x[i,j] for i in tipos_i for j in horarios_j)
)

# Resolver e imprimir solucion
solution = mdl.solve(log_output=True)

print(solution)