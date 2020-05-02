import Config
from Villager import Villager
from Compatibility import Compatibility
import pandas as pd
import numpy as np


def getVillagerByName(df, name):
    return Villager(df.loc[df[Config.NAME] == name].values.squeeze())

def createCompatibilityMatix():
    compat = Compatibility()
    villagerDF = pd.read_csv(Config.VILLAGERS_DATA_SOURCE)
    villagerNames = villagerDF[Config.NAME]
    villagerColumns = list(villagerNames)
    villagerColumns.insert(0,"villager")
    villagers = []
    compatibilityMatrix = pd.DataFrame(np.zeros((len(villagerColumns)-1,len(villagerColumns))), columns=villagerColumns)
    compatibilityMatrix["villager"] = villagerNames
    compatibilityMatrix.set_index("villager")

    for i in range(len(villagerDF)):
        villagers.append(Villager(villagerDF.loc[i].values.squeeze()))
    

    for i in range(len(villagers)):
        for j in range(i):
            compatibilityRating = compat.calculate(villagers[i],villagers[j])
            if compatibilityRating != 0:
                compatibilityMatrix.iloc[i,j+1] = compatibilityRating
                compatibilityMatrix.iloc[j,i+1] = compatibilityRating
        print("Calculating for " + villagers[i].name)
    
    compatibilityMatrix.to_csv(Config.COMPATIBILITY_DATA_SOURCE) 



createCompatibilityMatix()
