## ===================== ##
# ------ MODELO
## ===================== ##
import numpy as np
from docplex.mp.model import Model

mdl = Model(name='Contratación de personal')

def contratacion_personal(mdl):
    ## ========================================== ##
    # ------ Formulación matemática
    ## ========================================== ##

    # Parámetros y Datos
    semanas_t = range(4)  # t = 0, 1, 2, 3 (semanas 1, 2, 3, 4)
    demanda = [52, 65, 70, 85]

    # Variables de decisión
    N = mdl.integer_var_list(semanas_t, lb=0, name='N')           # Novatos
    A = mdl.integer_var_list(semanas_t, lb=0, name='A')           # Aprendices
    E = mdl.integer_var_list(semanas_t, lb=0, name='E')           # Total de Expertos
    E_prod = mdl.integer_var_list(semanas_t, lb=0, name='E_prod') # Expertos solo producción
    E_cap = mdl.integer_var_list(semanas_t, lb=0, name='E_cap')   # Expertos capacitan
    I = mdl.integer_var_list(semanas_t, lb=0, name='I')           # Inventario final

    ## ========================================== ##
    # ------ Restricciones
    ## ========================================== ##

    # 1. Descomposición y capacidad de expertos
    mdl.add_constraints([E[t] == E_prod[t] + E_cap[t] for t in semanas_t])
    mdl.add_constraints([N[t] <= 2 * E_cap[t] for t in semanas_t])

    # 2. Balance de personal
    # Semana 1 (t = 0)
    mdl.add_constraint(E[0] == 6)
    mdl.add_constraint(A[0] == 0)

    # Semanas 2, 3 y 4 (t = 1, 2, 3)
    mdl.add_constraints([A[t] == N[t - 1] for t in range(1, 4)])
    mdl.add_constraints([E[t] == E[t - 1] + A[t - 1] for t in range(1, 4)])

    # 3. Balance de inventario y producción
    # Producción t = 10*E_prod + 5*E_cap + 5*A + 1*N
    # Semana 1 (t = 0) con I_0 = 0
    mdl.add_constraint(10 * E_prod[0] + 5 * E_cap[0] + 5 * A[0] + 1 * N[0] == demanda[0] + I[0])

    # Semanas 2, 3 y 4 (t = 1, 2, 3)
    mdl.add_constraints([
        (10 * E_prod[t] + 5 * E_cap[t] + 5 * A[t] + 1 * N[t]) + I[t - 1] == demanda[t] + I[t]
        for t in range(1, 4)
    ])

    # 4. Condiciones de cierre (semana 4 / t = 3)
    mdl.add_constraint(N[3] == 0)  # Sin novatos en semana 4
    mdl.add_constraint(N[2] == 0)  # Sin aprendices en semana 4 (A[3] = N[2] = 0)
    
    # Al final de la semana 4 los expertos son E[3] + A[3]
    mdl.add_constraint(E[3] + A[3] >= 9)  # Al menos 9 expertos al final

    ## ========================================== ##
    # ------ Función Objetivo
    ## ========================================== ##
    mdl.minimize(
        mdl.sum(300 * E_prod[t] + 400 * E_cap[t] + 150 * A[t] + 50 * N[t] for t in semanas_t)
    )

    # Resolver e imprimir solución
    solution = mdl.solve(log_output=True)

    return solution


if __name__ == "__main__":
    solution = contratacion_personal(mdl)
    print(solution)