from Config import *
import pandas as pd
import time

class VillageOrganizer():
    def __init__(self):
        # Import a pre-computer compatibility graph
        self.compatibilityGraph = pd.read_csv(COMPATIBILITY_DATA_SOURCE,index_col=0)

        # Store a references to the villager names for later use
        self.villagerNames = self.compatibilityGraph.columns[1:]

        # Trim off the first column (villager name for that record)
        # and convert to a numpy array
        self.compatibilityGraph = self.compatibilityGraph[self.villagerNames].values

        self.CURRENT_BEST = 0
        self.SOLUTION_QUEUE = []


    def cost(self,village):
        #add up each villager's compatibility with each other villager
        c = 0
        for i in range(len(village)):
            for j in range(i):
                c = c + self.compatibilityGraph[village[i],village[j]]
        return c

    def promising(self,village, optimizer):
        # if the current compatibility is the same or better than the current best,
        # then the solution is promising
        potentialSolutions = []
        # check the potential compatibility of every villager not in the village
        for i in range(len(self.compatibilityGraph)):
            if not i in village:
                candidate = village + [i]

                # calculate the cost of the potential village
                potential = self.cost(candidate)

                # if the candidate solution is equivalent to the current best solution,
                # add it to the list of potentialSolutions
                if self.CURRENT_BEST == potential:
                    # print("Found similarly good")
                    potentialSolutions.append(candidate)

                # if the candidate solution is better than the current best solution,
                # recreate the list of potentialSolutions, and update the current best solution
                elif optimizer(potential,self.CURRENT_BEST) == potential:
                    # print("found new best")
                    self.CURRENT_BEST = potential
                    potentialSolutions = [candidate]
                    print(str([self.villagerNames[index] for index in candidate]) + " score: " + str(potential))

                # otherwise, the potential solution was worse than the current best solution.
                # The branch is pruned.

        return potentialSolutions

    def optimalVillage(self,village, optimizer):
        '''
            Recursively compute the optimal village
        '''

        #initial run
        potentialSolutions = self.promising(village, optimizer)
        self.SOLUTION_QUEUE = self.SOLUTION_QUEUE + potentialSolutions

        #keeping track of the best complete solutions
        completeSolutions = []
        bestCompleteCost = 0

        while len(self.SOLUTION_QUEUE):
            # pop solutions out of the queue for breadth first search
            currentSolution = self.SOLUTION_QUEUE.pop(0)

            # keep track of final solutions
            if len(currentSolution) == 10:
                currentCompleteCost = self.cost(currentSolution)

                #update best complete cost as better final solutions are found
                if bestCompleteCost == currentCompleteCost:
                    completeSolutions = completeSolutions + [currentSolution]
                elif optimizer(currentCompleteCost,bestCompleteCost) == currentCompleteCost:
                    completeSolutions = [currentSolution]
                    bestCompleteCost = currentCompleteCost

            # continue to solve partial solutions
            else:
                potentialSolutions = self.promising(currentSolution,optimizer)
                self.SOLUTION_QUEUE = self.SOLUTION_QUEUE + potentialSolutions

        #return best complete solutions
        return completeSolutions

        
V = VillageOrganizer()

'''
start_time = time.time()
chaoticVillage = V.optimalVillage([],min)
print("--- %s seconds ---" % (time.time() - start_time))

for v in chaoticVillage:
    v.sort()

for v in chaoticVillage:
    print(str([V.villagerNames[i] for i in v]) + " " + str(V.cost(v)))
'''

start_time = time.time()
peacefulVillage = V.optimalVillage([],max)
print("--- %s seconds ---" % (time.time() - start_time))

for v in peacefulVillage:
    v.sort()

for v in peacefulVillage:
    print(str([V.villagerNames[i] for i in v]) + " " + str(V.cost(v)))

