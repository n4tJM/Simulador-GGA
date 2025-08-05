from simulador import crossover_operators, mutation_operators, genetic_algorithm, solution
from interfaz import algoritmo_genetico, interfaz_base, panel_conceptos, simulador_genetico
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def main():
    app = interfaz_base.InterfazBase()
    app.mainloop()

if __name__ == "__main__":
    main()
 