import numpy as np
import random

class Solution:
    # Input: instance: matrix with the time it takes each machine to process each job. vector_machines: vector with the machines of the problem. n_jobs: number of jobs. n_machines: number of machines.
    #Methods: RandomStrategy(), MinStrategy(), BestStrategy(), Evaluate(), Validate(), Print()
    # Output: solution
    def __init__(self, instance, vector_machines, n_jobs: int, n_machines: int):
        self.n_jobs = n_jobs                    #Number of jobs
        self.n_machines = n_machines            #Number of machines
        self.instance = instance                #Instance to solve
        self.vector_Cis = []                    #vector to save the quality of the machines
        self.fitness = 0                        #Quality of the solution
        self.vector_machines = vector_machines  #vector with the machines to allocate the jobs
        self.vector_missed_jobs=[]             #vector with the jobs unallocated


    def RandomStrategy(self):
        # Generates a random solution.
        # Initialize vector_Cis and vector_machines
        for x in range(self.n_machines):
            self.vector_Cis.append(0)
            self.vector_machines.append([])
        # Generate a random assignment
        random_vector = np.random.randint(self.n_machines, size=self.n_jobs)
        for job in range(self.n_jobs):
            self.vector_machines[random_vector[job]].append(job)
            self.vector_Cis[random_vector[job]] = self.vector_Cis[random_vector[job]] + self.instance[job][random_vector[job]]

    def MinStrategy(self):
        # Generates a solution with a permutation of the jobs and then allocates them with the min() heuristic.
        # Initialize vectors vector_Cis and vector_machines
        for x in range(self.n_machines):
            self.vector_Cis.append(0)
            self.vector_machines.append([])
        # Generate a permutation of the jobs
        initial_vector = np.arange(0, self.n_jobs)
        random.shuffle(initial_vector)
        for j in range(0, self.n_jobs):
            job = initial_vector[j]
            index_min_machine = 0
            ci_min_machine = self.vector_Cis[index_min_machine]
            for machine in range(1, self.n_machines):
              if self.vector_Cis[machine] + self.instance[job][machine] <  ci_min_machine:
                index_min_machine = machine
                ci_min_machine = self.vector_Cis[index_min_machine]
            self.vector_machines[index_min_machine].append(job)
            self.vector_Cis[index_min_machine] = self.vector_Cis[index_min_machine] + self.instance[job][index_min_machine]

    def ShortestMinLBStrategy(self):
        # Generate a solution by sorting the jobs based on their shortest time and allocating them to the fastest machine until they reach a lower bound lb. Finally, it uses the min() heuristic to allocate the remaining jobs.
        # Initialize vectors vector_Cis and vector_machines
        for x in range(self.n_machines):
            self.vector_Cis.append(0)
            self.vector_machines.append([])
        #Generates a vector with the shortest time of every job
        vector_shortest_times = []
        vector_fastest_machine = []
        lb = 0

        for job in range (0, self.n_jobs):
            #print("job: ", job)
            #print(self.instance[job])
            index_shortest = 0
            for machine in range(1, self.n_machines):
              if self.instance[job][machine] < self.instance[job][index_shortest]:
                index_shortest = machine

            vector_shortest_times.append(self.instance[job][index_shortest])
            #print("min: ", vector_shortest_times[job])
            #print("se agregó: ", vector_shortest_times)
            vector_fastest_machine.append(index_shortest)
            lb = lb + self.instance[job][index_shortest]
        lb = lb / self.n_machines


        for job in range(0, self.n_jobs):
          if self.vector_Cis[vector_fastest_machine[job]] + self.instance[job][vector_fastest_machine[job]] <  lb:
            self.vector_machines[vector_fastest_machine[job]].append(job)
            self.vector_Cis[vector_fastest_machine[job]] = self.vector_Cis[vector_fastest_machine[job]] + self.instance[job][vector_fastest_machine[job]]
          else:
            self.vector_missed_jobs.append(job)
        self.MinHeuristic()

    def MinHeuristic(self):
        random.shuffle(self.vector_missed_jobs)
        for job in range(0, len(self.vector_missed_jobs)):
          index_min_machine = 0
          ci_min_machine = self.vector_Cis[index_min_machine]
          for machine in range(1, self.n_machines):
              if self.vector_Cis[machine] + self.instance[job][machine] <  ci_min_machine:
                index_min_machine = machine
                ci_min_machine = self.vector_Cis[index_min_machine]
          self.vector_machines[index_min_machine].append(job)
          self.vector_Cis[index_min_machine] = self.vector_Cis[index_min_machine] + self.instance[job][index_min_machine]
        self.vector_missed_jobs = []



    #General methods
    def Evaluate(self):
        self.fitness = self.vector_Cis[0]
        for i in range(1, self.n_machines):
            if self.vector_Cis[i] > self.fitness:
                self.fitness = self.vector_Cis[i]

    def Validate(self):
        count_jobs = 0
        ban = True
        # Verify that all jobs are assigned
        for machine in self.vector_machines:
            for job in machine:
                count_jobs = count_jobs + 1
        if count_jobs != self.n_jobs:
            ban = False
        # Cis validation
        Cis = np.zeros(self.n_machines)
        index_machine = 0
        for machine in self.vector_machines:
            for job in machine:
                Cis[index_machine] = Cis[index_machine] + self.instance[job][index_machine]
            if Cis[index_machine] != self.vector_Cis[index_machine]:
                ban = False
            index_machine = index_machine + 1
        # Print validation
        if ban:
            print("Right solution")
        else:
            print("Error, only ", count_jobs, " jobs were assigned")