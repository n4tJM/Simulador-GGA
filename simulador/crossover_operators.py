import numpy as np
from copy import copy
from simulador.solution import Solution

class CrossoverOperators:
    @staticmethod
    def OnePointCrossover(self, p1, p2):
        # Uses two parents to generate two children.

        # Determine cut-off point
        c_point = np.random.randint(1, self.machines - 1)

        # Initializing variables for children
        s1 = Solution(self.instance, [], self.jobs, self.machines)
        s2 = Solution(self.instance, [], self.jobs, self.machines)
        
        control_child1 = np.ones(self.jobs)
        control_child2 = np.ones(self.jobs)
        s1.vector_Cis = np.zeros(self.machines)
        s2.vector_Cis = np.zeros(self.machines)


        # Genetic material transmission
        for group in range(0, self.machines):
            if group <= c_point:
                # Transmit the groups on the left side of the cut point from parent1 to child1.
                s1.vector_machines.append([])
                for j in self.orderedPopulation[p1].vector_machines[group]:
                    s1.vector_machines[group].append(j)
                    control_child1[j] = 0
                s1.vector_Cis[group] = self.orderedPopulation[p1].vector_Cis[group]

                # Transmit the elements on the left side of the cut point from parent2 to child2.
                s2.vector_machines.append([])
                for j in self.orderedPopulation[p2].vector_machines[group]:
                    s2.vector_machines[group].append(j)
                    control_child2[j] = 0
                s2.vector_Cis[group] = self.orderedPopulation[p2].vector_Cis[group]
            else:
                s1.vector_machines.append([])
                s2.vector_machines.append([])
                # Child1 receives the groups on the right side of parent2.
                update_Ci = 0
                for j in self.orderedPopulation[p2].vector_machines[group]:
                    if control_child1[j] == 1:
                        s1.vector_machines[group].append(j)
                        control_child1[j] = 0
                        update_Ci = update_Ci + self.instance[j][group]
                s1.vector_Cis[group] = update_Ci

                # Child2 receives the groups on the right side of parent1.
                update_Ci = 0
                for j in self.orderedPopulation[p1].vector_machines[group]:
                    if control_child2[j] == 1:
                        s2.vector_machines[group].append(j)
                        control_child2[j] = 0
                        update_Ci = update_Ci + self.instance[j][group]
                s2.vector_Cis[group] = update_Ci

        # Repair strategy Children
        for job in range(0, self.jobs):
            if control_child1[job] == 1:
              s1.vector_missed_jobs.append(job)
            if control_child2[job] == 1:
              s2.vector_missed_jobs.append(job)
        s1.MinHeuristic()
        s2.MinHeuristic()
        # Children evaluation.
        s1.Evaluate()
        s2.Evaluate()
        #s1.Validate()
        #s2.Validate()
        #s1.PrintCompleteSolution()
        #s2.PrintCompleteSolution()

        # Update the number of evaluations
        self.evaluations = self.evaluations + 2
        # Add the children to the children[] list
        self.children.append(s1)
        self.children.append(s2)

    @staticmethod
    def TwoPointCrossover(self, p1, p2):
        # Recombines 2 parents to generate 2 children using two breakpoints
        c_point = np.random.randint(1, self.machines - 1)

        # Determine cut-off point
        cut_points = sorted(np.random.choice(range(1, self.machines), 2, replace=False))
        cut1, cut2 = cut_points[0], cut_points[1]

        # Initializing variables for children
        s1 = Solution(self.instance, [], self.jobs, self.machines)
        s2 = Solution(self.instance, [], self.jobs, self.machines)
        control_child1 = np.ones(self.jobs)
        control_child2 = np.ones(self.jobs)
        s1.vector_Cis = np.zeros(self.machines)
        s2.vector_Cis = np.zeros(self.machines)

        # Genetic material transmission
        for group in range(0, self.machines):
            if group < cut1 or group >= cut2:
                # The first parent transfers to s1 and the second parent to s2.
                s1.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p1].vector_machines[group]:
                    if control_child1[j] == 1:
                        s1.vector_machines[group].append(j)
                        control_child1[j] = 0
                        update_Ci += self.instance[j][group]
                s1.vector_Cis[group] = update_Ci

                s2.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p2].vector_machines[group]:
                    if control_child2[j] == 1:
                        s2.vector_machines[group].append(j)
                        control_child2[j] = 0
                        update_Ci += self.instance[j][group]
                s2.vector_Cis[group] = update_Ci
            else:
                # Intermediate segment: first parent transfers to s2 and second parent to s1.
                s1.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p2].vector_machines[group]:
                    if control_child1[j] == 1:
                        s1.vector_machines[group].append(j)
                        control_child1[j] = 0
                        update_Ci += self.instance[j][group]
                s1.vector_Cis[group] = update_Ci

                s2.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p1].vector_machines[group]:
                    if control_child2[j] == 1:
                        s2.vector_machines[group].append(j)
                        control_child2[j] = 0
                        update_Ci += self.instance[j][group]
                s2.vector_Cis[group] = update_Ci

        # Repair strategy Children
        for job in range(0, self.jobs):
            if control_child1[job] == 1:
                s1.vector_missed_jobs.append(job)
            if control_child2[job] == 1:
                s2.vector_missed_jobs.append(job)
        s1.MinHeuristic()
        s2.MinHeuristic()

        # Children evaluation.
        s1.Evaluate()
        s2.Evaluate()
        s1.Validate()
        s2.Validate()
        s1.PrintCompleteSolution()
        s2.PrintCompleteSolution()

        # Update the number of evaluations
        self.evaluations += 2

        # Add the children to the children[] list
        self.children.append(s1)
        self.children.append(s2)

    @staticmethod
    def ThreePointCrossover(self, p1, p2):
        # Recombines 2 parents to generate 2 children using three breakpoints

        # Determine cut-off points
        cut_points = sorted(np.random.choice(range(1, self.machines), 3, replace=False))
        cut1, cut2, cut3 = cut_points

        # Initializing variables for children
        s1 = Solution(self.instance, [], self.jobs, self.machines)
        s2 = Solution(self.instance, [], self.jobs, self.machines)
        control_child1 = np.ones(self.jobs)
        control_child2 = np.ones(self.jobs)
        s1.vector_Cis = np.zeros(self.machines)
        s2.vector_Cis = np.zeros(self.machines)

        # Genetic material transmission
        for group in range(0, self.machines):
            if group < cut1 or (cut2 <= group < cut3):
                # First and third segments: parent1 → s1, parent2 → s2
                s1.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p1].vector_machines[group]:
                    if control_child1[j] == 1:
                        s1.vector_machines[group].append(j)
                        control_child1[j] = 0
                        update_Ci += self.instance[j][group]
                s1.vector_Cis[group] = update_Ci

                s2.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p2].vector_machines[group]:
                    if control_child2[j] == 1:
                        s2.vector_machines[group].append(j)
                        control_child2[j] = 0
                        update_Ci += self.instance[j][group]
                s2.vector_Cis[group] = update_Ci
            else:
                # Second segment: parent2 → s1, parent1 → s2
                s1.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p2].vector_machines[group]:
                    if control_child1[j] == 1:
                        s1.vector_machines[group].append(j)
                        control_child1[j] = 0
                        update_Ci += self.instance[j][group]
                s1.vector_Cis[group] = update_Ci

                s2.vector_machines.append([])
                update_Ci = 0
                for j in self.orderedPopulation[p1].vector_machines[group]:
                    if control_child2[j] == 1:
                        s2.vector_machines[group].append(j)
                        control_child2[j] = 0
                        update_Ci += self.instance[j][group]
                s2.vector_Cis[group] = update_Ci

        # Repair strategy for children
        for job in range(0, self.jobs):
            if control_child1[job] == 1:
                s1.vector_missed_jobs.append(job)
            if control_child2[job] == 1:
                s2.vector_missed_jobs.append(job)
        s1.MinHeuristic()
        s2.MinHeuristic()

        # Children evaluation
        s1.Evaluate()
        s2.Evaluate()

        # Update the number of evaluations
        self.evaluations += 2

        # Add the children to the children[] list
        self.children.append(s1)
        self.children.append(s2)

    @staticmethod
    def FourPointCrossover(self, p1, p2):
      # Recombines 2 parents to generate 2 children using four breakpoints

      # Determine cut-off points
      cut_points = sorted(np.random.choice(range(1, self.machines), 4, replace=False))
      cut1, cut2, cut3, cut4 = cut_points

      # Initializing variables for children
      s1 = Solution(self.instance, [], self.jobs, self.machines)
      s2 = Solution(self.instance, [], self.jobs, self.machines)
      control_child1 = np.ones(self.jobs)
      control_child2 = np.ones(self.jobs)
      s1.vector_Cis = np.zeros(self.machines)
      s2.vector_Cis = np.zeros(self.machines)

      # Genetic material transmission
      for group in range(0, self.machines):
          if group < cut1 or (cut2 <= group < cut3) or (cut4 <= group):
              # Segments where parent1 → s1 and parent2 → s2
              s1.vector_machines.append([])
              update_Ci = 0
              for j in self.orderedPopulation[p1].vector_machines[group]:
                  if control_child1[j] == 1:
                      s1.vector_machines[group].append(j)
                      control_child1[j] = 0
                      update_Ci += self.instance[j][group]
              s1.vector_Cis[group] = update_Ci

              s2.vector_machines.append([])
              update_Ci = 0
              for j in self.orderedPopulation[p2].vector_machines[group]:
                  if control_child2[j] == 1:
                      s2.vector_machines[group].append(j)
                      control_child2[j] = 0
                      update_Ci += self.instance[j][group]
              s2.vector_Cis[group] = update_Ci
          else:
              # Segments where parent2 → s1 and parent1 → s2
              s1.vector_machines.append([])
              update_Ci = 0
              for j in self.orderedPopulation[p2].vector_machines[group]:
                  if control_child1[j] == 1:
                      s1.vector_machines[group].append(j)
                      control_child1[j] = 0
                      update_Ci += self.instance[j][group]
              s1.vector_Cis[group] = update_Ci

              s2.vector_machines.append([])
              update_Ci = 0
              for j in self.orderedPopulation[p1].vector_machines[group]:
                  if control_child2[j] == 1:
                      s2.vector_machines[group].append(j)
                      control_child2[j] = 0
                      update_Ci += self.instance[j][group]
              s2.vector_Cis[group] = update_Ci

      # Repair strategy for children
      for job in range(0, self.jobs):
          if control_child1[job] == 1:
              s1.vector_missed_jobs.append(job)
          if control_child2[job] == 1:
              s2.vector_missed_jobs.append(job)
      s1.MinHeuristic()
      s2.MinHeuristic()

      # Children evaluation
      s1.Evaluate()
      s2.Evaluate()

      # Update the number of evaluations
      self.evaluations += 2

      # Add the children to the children[] list
      self.children.append(s1)
      self.children.append(s2)

    @staticmethod
    def MultiPointCrossover(self, p1, p2, num_points):
      # Recombines 2 parents to generate 2 children using multiple breakpoints

      # Determine cut-off points
      cut_points = sorted(np.random.choice(range(1, self.machines), num_points, replace=False))

      # Initializing variables for children
      s1 = Solution(self.instance, [], self.jobs, self.machines)
      s2 = Solution(self.instance, [], self.jobs, self.machines)
      control_child1 = np.ones(self.jobs)
      control_child2 = np.ones(self.jobs)
      s1.vector_Cis = np.zeros(self.machines)
      s2.vector_Cis = np.zeros(self.machines)

      # Alternating between parents in each segment
      parent_switch = 0
      for group in range(0, self.machines):
          if parent_switch % 2 == 0:
              parent1, parent2 = p1, p2
          else:
              parent1, parent2 = p2, p1

          if group in cut_points:
              parent_switch += 1

          # Genetic material transmission
          s1.vector_machines.append([])
          update_Ci = 0
          for j in self.orderedPopulation[parent1].vector_machines[group]:
              if control_child1[j] == 1:
                  s1.vector_machines[group].append(j)
                  control_child1[j] = 0
                  update_Ci += self.instance[j][group]
          s1.vector_Cis[group] = update_Ci

          s2.vector_machines.append([])
          update_Ci = 0
          for j in self.orderedPopulation[parent2].vector_machines[group]:
              if control_child2[j] == 1:
                  s2.vector_machines[group].append(j)
                  control_child2[j] = 0
                  update_Ci += self.instance[j][group]
          s2.vector_Cis[group] = update_Ci

      # Repair strategy for children
      for job in range(0, self.jobs):
          if control_child1[job] == 1:
              s1.vector_missed_jobs.append(job)
          if control_child2[job] == 1:
              s2.vector_missed_jobs.append(job)
      s1.MinHeuristic()
      s2.MinHeuristic()

      # Children evaluation
      s1.Evaluate()
      s2.Evaluate()

      # Update the number of evaluations
      self.evaluations += 2

      # Add the children to the children[] list
      self.children.append(s1)
      self.children.append(s2)


    @staticmethod
    def UniformCrossover(self, p1, p2):
        # Recombine the genetic material of 2 parents to generate 2 children.

        # generate 2 objects of solution class
        s1 = Solution(self.instance, [], self.jobs, self.machines)
        s2 = Solution(self.instance, [], self.jobs, self.machines)

        # Variables initialization
        control_child1 = np.ones(self.jobs)
        control_child2 = np.ones(self.jobs)
        s1.vector_Cis = np.zeros(self.machines)
        s2.vector_Cis = np.zeros(self.machines)
    
        # Genetic material transmission
        for group in range(0, self.machines):
            # if probability > 0.5, parents p1 and p2 transmit the group to children s1 and s2, respectively. Otherwise, p1 transmits to child s2 and parent p2 to chil s1.
            if np.random.rand() <= 0.5:
                # child 1 inherits from parent 1
                s1.vector_machines.append([])

                update_Ci = 0
                for j in p1.vector_machines[group]:
                    if control_child1[j] == 1:
                        s1.vector_machines[group].append(j)
                        control_child1[j] = 0
                        update_Ci = update_Ci + self.instance[j][group]
                s1.vector_Cis[group] = update_Ci

                # child 2 inherits from parent 2
                s2.vector_machines.append([])
                update_Ci = 0
                for j in p2.vector_machines[group]:
                    if control_child2[j] == 1:
                        s2.vector_machines[group].append(j)
                        control_child2[j] = 0
                        update_Ci = update_Ci + self.instance[j][group]
                s2.vector_Cis[group] = update_Ci
            else:
                s1.vector_machines.append([])
                s2.vector_machines.append([])
                # child 1 inherits from parent 2
                update_Ci = 0
                for j in p2.vector_machines[group]:
                    if control_child1[j] == 1:
                        s1.vector_machines[group].append(j)
                        control_child1[j] = 0
                        update_Ci = update_Ci + self.instance[j][group]
                s1.vector_Cis[group] = update_Ci

                # child 2 inherits from parent 2.
                update_Ci = 0
                for j in p1.vector_machines[group]:
                    if control_child2[j] == 1:
                        s2.vector_machines[group].append(j)
                        control_child2[j] = 0
                        update_Ci = update_Ci + self.instance[j][group]
                s2.vector_Cis[group] = update_Ci

        # Repair strategy Children
        for job in range(0, self.jobs):
            if control_child1[job] == 1:
              s1.vector_missed_jobs.append(job)
            if control_child2[job] == 1:
              s2.vector_missed_jobs.append(job)
        s1.MinHeuristic()
        s2.MinHeuristic()
        s1.Evaluate()
        s2.Evaluate()
        #s1.Validate()
        #s2.Validate()
        #s1.PrintCompleteSolution()
        #s2.PrintCompleteSolution()

        # Update the number of evaluations
        self.evaluations = self.evaluations + 2

        # Add children to the list children[]
        self.children.append(s1)
        self.children.append(s2)

    def ReplacementWorst(self):
        # Children replace the worst solutions.
        for x in range(0, len(self.children)):
            self.orderedPopulation[self.pSize - 1 - x] = copy.deepcopy(self.children[x])

        # Clean variables
        self.population = []
        self.population = copy.deepcopy(self.orderedPopulation)
        self.orderedPopulation = []
        self.children = []
        self.parents = []

    