# Import functions from the docplex module
from docplex.mp.model import Model

def bin_packing(pesos, capacidad, homo=True):
    mdl = Model(name='P empaquetamiento')
    obj = [(i) for i in range(len(pesos))] # objetos
    contenedores = [(j) for j in range(len(capacidad))] #Contenedores

    x = mdl.binary_var_matrix(obj,contenedores,name='x')
    y = mdl.binary_var_list(contenedores,name='y')

    if homo:
        mdl.add_constraints(
            mdl.sum(pesos[i]*x[i,j] for i in obj) <= (capacidad*y[j]) for j in contenedores
            )
    else: # no homo
        mdl.add_constraints(
            mdl.sum(pesos[i]*x[i,j] for i in obj) <= (capacidad[j]*y[j]) for j in contenedores
            )

    mdl.add_constraints(
        mdl.sum(x[i,j] for j in contenedores) == 1 for i in obj
    )

    mdl.minimize(
        mdl.sum(y[j] for j in contenedores)
        )

    solution = mdl.solve(log_output=True,)
    return solution