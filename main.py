import Config
from Villager import Villager
from Compatibility import Compatibility
import pandas as pd
import numpy as np
villagerDF = pd.read_csv(Config.VILLAGERS_DATA_SOURCE)
villagerNames = list(villagerDF[Config.NAME])
compat = Compatibility()

def getVillagerByName(df, name):
    return Villager(df.loc[df[Config.NAME] == name].values.squeeze())

def createCompatibilityMatix(villagers):
    '''
        Create a table of the compatibility between each villager and each other individual villager.
    '''

    #Set up the compatibility matrix dataframe
    villagerColumns = [v.name for v in villagers]
    villagerColumns.insert(0,"villager")
    compatibilityMatrix = pd.DataFrame(np.zeros((len(villagerColumns)-1,len(villagerColumns))), columns=villagerColumns)
    compatibilityMatrix["villager"] = villagerColumns[1:]
    compatibilityMatrix.set_index("villager")


    for i in range(len(villagers)):
        for j in range(i):
            #Compare each villager to each other villager
            compatibilityRating = compat.calculate(villagers[i],villagers[j])
            if compatibilityRating != 0:
                #No need to do unnecessary updates, as everything starts at 0
                #Matrix is symetric, update both values in one cycle
                compatibilityMatrix.iloc[i,j+1] = compatibilityRating
                compatibilityMatrix.iloc[j,i+1] = compatibilityRating
        print("Calculating for " + villagers[i].name)
    return compatibilityMatrix

def villageCompatibility(villagerList, verbose=Config.VERBOSE):
    '''
        calculate and aggregate the compatibility score between each villager
    '''
    compatScalar = 0
    if verbose:
        print("villager1, villager2: score")
    for i in range(len(villagerList)):
        for j in range(i):
            #Calculate and add
            relation = compat.calculate(villagerList[i],villagerList[j])
            compatScalar = compatScalar + relation
            if verbose:
                print("%s, %s: %s" % (villagerList[i].name, villagerList[j].name, str(relation)))


    return compatScalar

def createVillage(nameList):
    '''
        create a list of villager objects
    '''
    #Get the records associated with the list of names provided
    villagerValues = villagerDF[villagerDF["Name"].isin(nameList)].values

    #list comprehension to create villager object for each name/record
    village = [Villager(villagerValues[i]) for i in range(len(nameList))]

    return village

def optimizeVillageWalk(optimizer, village, notVillage):
    '''
        Create a semi-optimized village, when supplied an optimizer function (max/min) and a list of villagers
    '''
    if Config.DEBUG:
        print("Optimizing on Village: " + str(village) + " of size " 
                + str(len(village)) +  " with score " + str(villageCompatibility(village, verbose=False)))
    optimalScore = 0
    best = []
    if len(village) == Config.MAX_VILLAGE_SIZE:
        #The village is full
        return [village] #?

    for outsider in notVillage:
        communityModificationScore = 0


        #calculate the community modification score for this outsider
        communityModificationScore = sum([compat.calculate(outsider, villager) for villager in village])

        if optimalScore == communityModificationScore:
            #This optimal score is equivalent to the community score, equivalent candidates
            #append this candidate to the list of potential best candidates
            best.append(outsider)

        elif optimizer(communityModificationScore,optimalScore) == communityModificationScore:
            #This candidate is a new best
            #remove other candidates from the list, and update the optimal score
            optimalScore = communityModificationScore
            best = [outsider]
    #At this point in time, best is a list of villagers with equivalently optimal scores

    #find all potential optimal villages from this node
    potentialVillages = [optimizeVillageWalk(optimizer, village + [villager],
                            [outsider for outsider in notVillage if outsider != villager]) for villager in best][0]
    #NOTE: to prevent a typing mismatch between returning base case singleton village of length 10, and list of villages
        #(optimal villages), singleton village is placed in a shell list. the [0] at the end of the previous statement removes the shell
    potentialCompatibilities = [villageCompatibility(pv,verbose=False) for pv in potentialVillages]
    optimalCompatibility = optimizer(potentialCompatibilities)
    optimalVillages = [potentialVillages[i] for i in range(len(potentialVillages)) if potentialCompatibilities[i] == optimalCompatibility]
    #return the list of optimalVillages
    return optimalVillages

verbose = False
myCurrentVillagerNames = [] # ["Merengue","Puck","Curlos","Monique","Hamlet"]
notInVillage = [name for name in villagerNames if name not in myCurrentVillagerNames]
myCurrentVillage = createVillage(myCurrentVillagerNames)
notMyCurrentVillage = createVillage(notInVillage)

#print("Overall Score: %s" % villageCompatibility(myCurrentVillage,verbose=verbose))
optimalVillages = optimizeVillageWalk(min, myCurrentVillage,notMyCurrentVillage)
print("Optimal Village(s): ")
for v in optimalVillages:
    print(str(v) + " with score: " + str(villageCompatibility(v,verbose=False)))
