from docplex.mp.model import Model
import numpy as np
import numpy as np


def sudoku(cuadrantes: list):     
    mdl = Model(name='Sudoku')

    I_i = range(3)        # renglón dentro del bloque
    J_j = range(3)        # columna dentro del bloque
    K_k = range(1, 10)    # número 1..9
    
    # ===== Variables de decision =====
    
    a, b, c, d, e, f, g, h, i = [mdl.binary_var_cube(I_i, J_j, K_k, name=n)
                             for n in 'abcdefghi']
    
    bloques = [a, b, c, d, e, f, g, h, i]
    
    # ===== Restricciones: filas =====
    
    filas_de_bloques = [(a, b, c),
                    (d, e, f),
                    (g, h, i)]

    # en la primera vuelta x, y, z = a, b, c, en la segunda d, e, f, etc. 
    for x, y, z in filas_de_bloques:
        for m in I_i:
            for k in K_k:
                mdl.add_constraint(
                    mdl.sum(x[m, j, k] + y[m, j, k] + z[m, j, k] for j in J_j) == 1
                    )
                
                
    # ===== Restricciones: columnas =====
        
    columnas_de_bloques = [(a, d, g),
                           (b, e, h),
                           (c, f, i)]

    for x, y, z in columnas_de_bloques:
        for j in J_j:
            for k in K_k:
                mdl.add_constraint(
                    mdl.sum(x[m, j, k] + y[m, j, k] + z[m, j, k] for m in I_i) == 1
                    )
                    
    # ===== Restricciones: cuadrito =====

    for p in bloques: 
        for k in K_k:
            mdl.add_constraint(mdl.sum(p[m,j,k] for m in I_i for j in J_j) == 1)
            
    # ===== Restricciones: cuadricula =====
    
    for p in bloques: 
        for m in I_i:
            for j in J_j:
                mdl.add_constraint(mdl.sum(p[m,j,k] for k in K_k) == 1)
                
    # ==== Condiciones iniciales ==== 
    
    for blk, var in zip(cuadrantes, bloques):
        for m in I_i:
            for j in J_j:
                if blk[m][j] != 0:
                    mdl.add_constraint(var[m, j, blk[m][j]] == 1)
                    
    # ===== MODELO =====
    #mdl.print_information()
    
    # problema de factibilidad
    mdl.minimize(0)
    
    sol = mdl.solve(log_output=True)
    
    # construye 
    
    R = [leer_bloque(p, I_i, J_j, K_k) for p in bloques]

    solucion = np.block([[R[0], R[1], R[2]],
                        [R[3], R[4], R[5]],
                        [R[6], R[7], R[8]]])
    print("solucion: \n", solucion)

    return sol
    
    
def leer_bloque(var, I_i, J_j, K_k):
    """Convierte las variables de un bloque en una matriz 3x3 con los números."""
    M = np.zeros((3, 3), dtype=int)
    for m in I_i:
        for j in J_j:
            for k in K_k:
                if var[m, j, k].solution_value > 0.5:
                    M[m, j] = k
    return M