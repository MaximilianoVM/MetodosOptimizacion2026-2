# Import functions from the docplex module
from docplex.mp.model import Model

m = Model("Problema de asignacion")

# Conjuntos
profesor = [(i) for i in range(5)]  # A,B,C,D,E
curso = [(j) for j in range(5)]     # C1,C2,C3,C4,C5

# Parametros: p[i][j] = preferencia del profesor i por el curso j
#      C1 C2 C3 C4 C5
p = [[5, 7, 9, 8, 6],    # A
     [8, 2, 10, 7, 9],   # B
     [5, 3, 8, 9, 9],    # C
     [9, 6, 9, 7, 10],   # D
     [7, 8, 8, 8, 5]]    # E

# Definir variables de decision
x = m.binary_var_matrix(profesor, curso, name='x')

# Definir las restricciones
# Cada profesor debe tener un curso
m.add_constraints(m.sum(x[i,j] for j in curso) == 1 for i in profesor)

# Cada curso debe tener un profesor
m.add_constraints(m.sum(x[i,j] for i in profesor) == 1 for j in curso)

# Definir la funcion objetivo
m.maximize(m.sum(p[i][j]*x[i,j] for i in profesor for j in curso))

# Resolver e imprimir solucion
solution = m.solve(log_output=True,)
print(solution)

# Imprimir la asignacion
nombre_profesor = ['A','B','C','D','E']
nombre_curso = ['C1','C2','C3','C4','C5']

if solution:
   print("\nPreferencia total = ", m.objective_value)
   for i in profesor:
      for j in curso:
         if x[i,j].solution_value > 0.5:
            print("Profesor", nombre_profesor[i], "-> curso", nombre_curso[j],
                  "(preferencia", p[i][j], ")")

m.export_as_lp(path=".")
