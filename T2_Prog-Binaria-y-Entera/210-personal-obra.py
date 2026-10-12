## ===================== ##
# ------ MODELO
## ===================== ##
import numpy as np
from docplex.mp.model import Model

mdl = Model(name='Personal de obra')

def personal_obra(mdl, outsorcing=False):
    ## ========================================== ##
    # ------ Formulacion matematica
    ## ========================================== ##

    # Variables de decision 
    turnos_i = [1, 2, 3, 4, 5, 6]
    turnos_i = np.linspace(1, 6, 6, dtype=int)

    x = mdl.integer_var_list(turnos_i, lb=0, name='x')
    
    if outsorcing:
        y = mdl.integer_var_list(turnos_i, lb=0, name='y')

    ## ========================================== ##
    # ------ Restricciones
    ## ========================================== ##
    if outsorcing:
        mdl.add_constraints([
            x[5] + x[0] + y[0] >= 70,  # Turno 6 + Turno 1
            x[0] + x[1] + y[1] >= 20,  # Turno 1 + Turno 2
            x[1] + x[2] + y[2] >= 80,  # Turno 2 + Turno 3
            x[2] + x[3] + y[3] >= 30,  # Turno 3 + Turno 4
            x[3] + x[4] + y[4] >= 10,  # Turno 4 + Turno 5
            x[4] + x[5] + y[5] >= 10   # Turno 5 + Turno 6
        ])
    else: 
        mdl.add_constraints([
            x[5] + x[0] >= 70,  # Turno 6 + Turno 1
            x[0] + x[1] >= 20,  # Turno 1 + Turno 2
            x[1] + x[2] >= 80,  # Turno 2 + Turno 3
            x[2] + x[3] >= 30,  # Turno 3 + Turno 4
            x[3] + x[4] >= 10,  # Turno 4 + Turno 5
            x[4] + x[5] >= 10   # Turno 5 + Turno 6
        ])
    
    ## ========================================== ##
    # ------ Funcion Objetivo
    ## ========================================== ##
    # Funcion objetivo
    if outsorcing:
        mdl.minimize(
            mdl.sum( 8*(x[0] + x[1] + x[2])+ 10*x[3] + 14*x[4] + 12*x[5]
                    + 14.4*mdl.sum(y[i-1] for i in turnos_i) )
        )
    else:
        mdl.minimize(
            mdl.sum( 8*(x[0] + x[1] + x[2])+ 10*x[3] + 14*x[4] + 12*x[5] )
        )


    # Resolver e imprimir solucion
    solution = mdl.solve(log_output=True)
    
    return solution
    

if __name__ == "__main__":
    solution = personal_obra(mdl, outsorcing=True)
    print(solution)
    