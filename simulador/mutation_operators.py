import numpy as np
from simulador.solution import Solution


class MutationOperators:
    @staticmethod
    def SwapMutation(self, s):
        # Select two machines, from each machine select 1 jobs
        # Machines selection
        m1 = np.random.randint(0, self.machines)
        while len(s.vector_machines[m1]) == 0:
            m1 = np.random.randint(0, self.machines)

        m2 = np.random.randint(0, self.machines)
        while m1 == m2 or len(s.vector_machines[m2]) == 0:
            m2 = np.random.randint(0, self.machines)
        # Jobs selection
        ind_j1 = -1
        ind_j2 = -1
        if len(s.vector_machines[m1]) == 1:
            ind_j1 = 0
        else:
            ind_j1 = np.random.randint(0, len(s.vector_machines[m1]))

        if len(s.vector_machines[m2]) == 1:
            ind_j2 = 0
        else:
            ind_j2 = np.random.randint(0, len(s.vector_machines[m2]))

        j1= s.vector_machines[m1][ind_j1]
        j2= s.vector_machines[m2][ind_j2]
        #swap
        s.vector_Cis[m1] = s.vector_Cis[m1] - self.instance[j1][m1] + - self.instance[j2][m1]
        s.vector_machines[m1].append(j2)
        s.vector_Cis[m2] = s.vector_Cis[m2] - self.instance[j2][m2] + - self.instance[j1][m2]
        s.vector_machines[m2].append(j1)
        s.vector_machines[m1].remove(j1)
        s.vector_machines[m2].remove(j2)

        # Update fitness
        s.Evaluate()
        self.evaluations = self.evaluations + 1

    @staticmethod
    def InsertionMutation(self, s):
        # Selección de una máquina origen (m1) y una máquina destino (m2)
        m1 = np.random.randint(0, self.machines)
        while len(self.orderedPopulation[s].vector_machines[m1]) == 0:
            m1 = np.random.randint(0, self.machines)

        m2 = np.random.randint(0, self.machines)
        while m1 == m2:
            m2 = np.random.randint(0, self.machines)

        # Selección de un trabajo en m1
        ind_j1 = np.random.randint(0, len(self.orderedPopulation[s].vector_machines[m1]))
        j1 = self.orderedPopulation[s].vector_machines[m1][ind_j1]

        # Actualizar los tiempos de procesamiento
        self.orderedPopulation[s].vector_Cis[m1] -= self.instance[j1][m1]  # Remover trabajo de m1
        self.orderedPopulation[s].vector_Cis[m2] += self.instance[j1][m2]  # Agregar trabajo a m2

        # Mover el trabajo a la nueva máquina
        self.orderedPopulation[s].vector_machines[m1].remove(j1)
        self.orderedPopulation[s].vector_machines[m2].append(j1)

        # Actualizar fitness
        self.orderedPopulation[s].Evaluate()
        self.evaluations += 1

    @staticmethod
    def ItemEliminationMutation(self, s):
        # Seleccionar una máquina al azar con al menos un trabajo
        m1 = np.random.randint(0, self.machines)
        while len(self.orderedPopulation[s].vector_machines[m1]) == 0:
            m1 = np.random.randint(0, self.machines)

        # Seleccionar un trabajo al azar en m1
        ind_j1 = np.random.randint(0, len(self.orderedPopulation[s].vector_machines[m1]))
        j1 = self.orderedPopulation[s].vector_machines[m1][ind_j1]

        # Actualizar los tiempos de procesamiento eliminando el trabajo
        self.orderedPopulation[s].vector_Cis[m1] -= self.instance[j1][m1]

        # Remover el trabajo de la máquina
        self.orderedPopulation[s].vector_machines[m1].remove(j1)

        # Actualizar fitness
        self.orderedPopulation[s].Evaluate()
        self.evaluations += 1

    @staticmethod
    def EliminationMutation(self, s):
        # Seleccionar una máquina al azar con al menos un trabajo
        m1 = np.random.randint(0, self.machines)
        while len(self.orderedPopulation[s].vector_machines[m1]) == 0:
            m1 = np.random.randint(0, self.machines)

        # Obtener todos los trabajos en la máquina seleccionada
        jobs_to_remove = self.orderedPopulation[s].vector_machines[m1]

        # Actualizar tiempos de procesamiento
        for j in jobs_to_remove:
            self.orderedPopulation[s].vector_Cis[m1] -= self.instance[j][m1]

        # Vaciar la máquina
        self.orderedPopulation[s].vector_machines[m1] = []

        # Actualizar fitness
        self.orderedPopulation[s].Evaluate()
        self.evaluations += 1

    @staticmethod
    def MergeAndSplitMutation(self, s):
        # Seleccionar dos máquinas distintas con al menos un trabajo
        m1 = np.random.randint(0, self.machines)
        while len(self.orderedPopulation[s].vector_machines[m1]) == 0:
            m1 = np.random.randint(0, self.machines)

        m2 = np.random.randint(0, self.machines)
        while m1 == m2 or len(self.orderedPopulation[s].vector_machines[m2]) == 0:
            m2 = np.random.randint(0, self.machines)

        # Fusionar los trabajos de m1 y m2 en una sola lista
        merged_jobs = self.orderedPopulation[s].vector_machines[m1] + self.orderedPopulation[s].vector_machines[m2]

        # Vaciar ambas máquinas antes de redistribuir
        self.orderedPopulation[s].vector_machines[m1] = []
        self.orderedPopulation[s].vector_machines[m2] = []
        self.orderedPopulation[s].vector_Cis[m1] = 0
        self.orderedPopulation[s].vector_Cis[m2] = 0

        # Redistribuir los trabajos de manera aleatoria en m1 y m2
        np.random.shuffle(merged_jobs)  # Mezclar trabajos para una asignación más aleatoria
        split_point = len(merged_jobs) // 2  # Punto de división en dos partes

        self.orderedPopulation[s].vector_machines[m1] = merged_jobs[:split_point]
        self.orderedPopulation[s].vector_machines[m2] = merged_jobs[split_point:]

        # Recalcular los tiempos de procesamiento
        for j in self.orderedPopulation[s].vector_machines[m1]:
            self.orderedPopulation[s].vector_Cis[m1] += self.instance[j][m1]

        for j in self.orderedPopulation[s].vector_machines[m2]:
            self.orderedPopulation[s].vector_Cis[m2] += self.instance[j][m2]

        # Actualizar fitness
        self.orderedPopulation[s].Evaluate()
        self.evaluations += 1

    @staticmethod
    def ESXMutation(self, s):
        # Seleccionar dos máquinas distintas con al menos dos trabajos
        m1 = np.random.randint(0, self.machines)
        while len(self.orderedPopulation[s].vector_machines[m1]) < 2:
            m1 = np.random.randint(0, self.machines)

        m2 = np.random.randint(0, self.machines)
        while m1 == m2 or len(self.orderedPopulation[s].vector_machines[m2]) < 2:
            m2 = np.random.randint(0, self.machines)

        # Determinar el tamaño del segmento a intercambiar
        max_segment_size = min(len(self.orderedPopulation[s].vector_machines[m1]),
                              len(self.orderedPopulation[s].vector_machines[m2]))
        segment_size = np.random.randint(1, max_segment_size + 1)  # Al menos 1 trabajo

        # Seleccionar segmentos aleatorios en ambas máquinas
        segment_m1 = np.random.choice(self.orderedPopulation[s].vector_machines[m1], segment_size, replace=False).tolist()
        segment_m2 = np.random.choice(self.orderedPopulation[s].vector_machines[m2], segment_size, replace=False).tolist()

        # Intercambiar los segmentos entre las máquinas
        for job in segment_m1:
            self.orderedPopulation[s].vector_machines[m1].remove(job)
            self.orderedPopulation[s].vector_machines[m2].append(job)

        for job in segment_m2:
            self.orderedPopulation[s].vector_machines[m2].remove(job)
            self.orderedPopulation[s].vector_machines[m1].append(job)

        # Actualizar los tiempos de procesamiento
        self.orderedPopulation[s].vector_Cis[m1] = sum(self.instance[j][m1] for j in self.orderedPopulation[s].vector_machines[m1])
        self.orderedPopulation[s].vector_Cis[m2] = sum(self.instance[j][m2] for j in self.orderedPopulation[s].vector_machines[m2])

        # Evaluar la nueva solución
        self.orderedPopulation[s].Evaluate()
        self.evaluations += 1
