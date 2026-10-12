from docplex.mp.model import Model
import numpy as np

mdl = Model(name='Planeacion de horario')

# VARIABLES DE DECISION 

materias_i = range(8) 
aulas_j = range(3) 
horas_k = range(5)

x = mdl.binary_var_dict(
    [(i, j, k) for i in materias_i for j in aulas_j for k in horas_k], 
    name='x'
)

# RESTRICCIONES 

# grupos de materias por docente
docente_1 = [0, 1, 7]        # M1, M2, M8
docente_2 = [2, 3, 4, 5, 6]  # M3, M4, M5, M6, M7

curso_1 = [0, 1, 2, 3]       # M1, M2, M3, M4
curso_2 = [4, 5, 6, 7]       # M5, M6, M7, M8

# restriccion 1
mdl.add_constraints(
    mdl.sum(x[i, j, k] for j in aulas_j for k in horas_k) == 1
    for i in materias_i
)

# restriccion 2
mdl.add_constraints(mdl.sum(x[i, j, k] for i in materias_i) <= 1
                    for j in aulas_j 
                    for k in horas_k 
                    )

# restriccion 3
for k in horas_k:
    mdl.add_constraint(mdl.sum(x[i, j, k] for i in docente_1 for j in aulas_j) <= 1)
    mdl.add_constraint(mdl.sum(x[i, j, k] for i in docente_2 for j in aulas_j) <= 1)
    
# restriccion 4
for k in horas_k:
    mdl.add_constraint(mdl.sum(x[i, j, k] for i in curso_1 for j in aulas_j) <= 1)
    mdl.add_constraint(mdl.sum(x[i, j, k] for i in curso_2 for j in aulas_j) <= 1)
    

# FUNCION OBJETIVO 
mdl.minimize(mdl.sum((k + 1) * x[i, j, k] for i in materias_i for j in aulas_j for k in horas_k))

solution = mdl.solve(log_output=True)

if solution:
    print(f"Valor óptimo de la función objetivo: {solution.objective_value}\n")
    print("=================== HORARIO ESCOLAR OPTIMIZADO ===================")
    for k in horas_k:
        print(f"\n--- Bloque {k + 1} ---")
        clases_en_bloque = 0
        for j in aulas_j:
            for i in materias_i:
                if x[i, j, k].solution_value > 0.5:
                    print(f"  Aula {j + 1}: Materia M{i + 1}")
                    clases_en_bloque += 1
        if clases_en_bloque == 0:
            print("  (Sin clases programadas)")