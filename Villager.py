import Config
import pandas as pd

class Villager():
    def __init__(self, villagerList):
        self.name = villagerList[0]
        self.personality = Villager.toPersonalityInt(villagerList[1])
        self.species = Villager.toSpeciesInt(villagerList[2])
        self.sign = Villager.toSignInt(villagerList[3])

    def __repr__(self):
        if Config.VERBOSE:
            return "%s %s %s %s" %(self.name, self.personality, self.species, self.sign)
        else:
            return self.name

    def toPersonalityInt(p):
         #convert personality to int as specified in config
         return Config.PERSONALITY_DICTIONARY[p]

    def toSpeciesInt(s):
        #Convert species to int as specified in config
        return Config.SPECIES_DICTIONARY[s] if s in Config.RELEVANT_SPECIES else 0

    def toSignInt(s):
        #Convert sign to int as specified in config
        return Config.SIGN_DICTIONARY[s]

