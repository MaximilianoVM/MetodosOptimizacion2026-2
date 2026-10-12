from docplex.mp.model import Model

mdl = Model(name='Camino_Mas_Corto')

# dic de arcos y costos
arcos_costos = {
    ('A', 'B'): 4,
    ('A', 'C'): 2,
    ('A', 'D'): 5,
    ('B', 'E'): 3,
    ('C', 'B'): 1,
    ('C', 'E'): 6,
    ('C', 'F'): 3,
    ('D', 'F'): 2,
    ('E', 'N'): 6,
    ('F', 'N'): 4
}

# nodos
nodos = ['A', 'B', 'C', 'D', 'E', 'F', 'N']

# vars de decision
x = mdl.binary_var_dict(arcos_costos.keys(), name='x')

# restricciones de flujo
for nodo in nodos:
    flujo_salida = mdl.sum(x[i, j] for i, j in arcos_costos.keys() if i == nodo)
    flujo_entrada = mdl.sum(x[i, j] for i, j in arcos_costos.keys() if j == nodo)
    
    if nodo == 'A':
        mdl.add_constraint(flujo_salida - flujo_entrada == 1)
    elif nodo == 'N':
        mdl.add_constraint(flujo_salida - flujo_entrada == -1)
    else:
        mdl.add_constraint(flujo_salida - flujo_entrada == 0)


# funcion objetivo
mdl.minimize(mdl.sum(costo * x[arc] for arc, costo in arcos_costos.items()))

# resolver
solution = mdl.solve(log_output=False)

if solution:
    print(f"longitud del camino mas corto: {solution.objective_value}")
    print("arcos usados en el camino:")
    for arc in arcos_costos.keys():
        if x[arc].solution_value > 0.5:
            print(f"  {arc[0]} -> {arc[1]} (Costo: {arcos_costos[arc]})")