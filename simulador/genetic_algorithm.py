from copy import deepcopy
from operator import attrgetter
import numpy as np
from simulador.solution import Solution
from simulador.crossover_operators import CrossoverOperators
from simulador.mutation_operators import MutationOperators



class GeneticAlgorithm:
    def __init__(self, instance, n_jobs: int, n_machines: int, p_size: int, p_gen: int, c_rate: float, m_rate: float):
        self.instance = instance
        self.jobs = n_jobs
        self.machines = n_machines
        
        # Parámetros configurables
        self.population_size = p_size
        self.max_generations = p_gen
        self.crossover_rate = c_rate
        self.mutation_rate = m_rate
        
        # Estado del algoritmo
        self.generation = 0
        self.population = []
        self.best_solution = None
        self.orderedPopulation = []
        self.evaluations = 0
        self.children = []

    def OrderPopulation(self):
        self.orderedPopulation = []
        self.orderedPopulation = deepcopy(sorted(self.population, key=attrgetter('fitness'), reverse=False))

    def ReplacementWorst(self):
        # Children replace the worst solutions.
        for x in range(0, len(self.children)):
            self.orderedPopulation[self.population_size - 1 - x] = deepcopy(self.children[x])

        # Clean variables
        self.population = []
        self.population = deepcopy(self.orderedPopulation)
        self.orderedPopulation = []
        self.children = []
        self.parents = []
        
    def initialize_population(self):
        self.population = []
        for _ in range(self.population_size):
            solution = Solution(self.instance, [], self.jobs, self.machines)
            solution.MinStrategy()
            solution.Evaluate()
            self.population.append(solution)
            self.evaluations += 1
        
        self._update_best_solution()

    def _update_best_solution(self):
        self.population.sort(key=lambda x: x.fitness)
        current_best = self.population[0]
        
        if self.best_solution is None or current_best.fitness < self.best_solution.fitness:
            self.best_solution = deepcopy(current_best)
    
    def selection(self):
        # Selección proporcional para minimización
        fitnesses = [1/s.fitness for s in self.orderedPopulation]
        total_fitness = sum(fitnesses)
        probabilities = [f/total_fitness for f in fitnesses]
        
        # Seleccionar padres
        parents = np.random.choice(
            self.orderedPopulation,
            size=int(self.crossover_rate * self.population_size),
            p=probabilities,
            replace=False
        )
        
        return parents
    
    def run_generation(self):
        self.OrderPopulation()
        # Selección
        parents = self.selection()
        
        # Cruza
        for i in range(0, len(parents), 2):
            if i+1 < len(parents):
                CrossoverOperators.UniformCrossover(
                    self, parents[i], parents[i+1])
        
        self.ReplacementWorst()
        self.OrderPopulation()


        # Mutación
        for i in range(int(self.mutation_rate * self.population_size)):
            idx = np.random.randint(len(self.population))
            MutationOperators.SwapMutation(self, self.orderedPopulation[idx])
        
        self._update_best_solution()
        self.generation += 1
    
    def run(self):
        self.initialize_population()

        while self.generation < self.max_generations:
            self.run_generation()
            # Opcional: imprimir progreso
            if self.generation % 10 == 0:
                print(f"Gen {self.generation}: Best fitness = {self.best_solution.fitness}")
        
        return self.best_solution