import Config
class Compatibility():
    def __init__(self):
        #DATA GATHERED FROM:
        # https://nookipedia.com/wiki/Compatibility

        self.PERSONALITY_COMPATABILITY = [
            [Config.CLUB],
            [Config.CROSS, Config.HEART],
            [Config.CROSS, Config.DIAMOND, Config.HEART],
            [Config.DIAMOND, Config.CROSS, Config.HEART, Config.HEART],
            [Config.HEART, Config.CLUB, Config.DIAMOND, Config.CROSS, Config.CLUB],
            [Config.CLUB, Config.DIAMOND, Config.CROSS, Config.CLUB, Config.HEART, Config.HEART],
            [Config.HEART, Config.CLUB, Config.CLUB, Config.DIAMOND, Config.DIAMOND, Config.CROSS, Config.HEART],
            [Config.DIAMOND, Config.HEART, Config.CLUB, Config.CLUB, Config.CROSS, Config.DIAMOND, Config.CROSS, Config.HEART]
            ]


        self.SPECIES_HEART = [
                Config.BEAR * Config.CUB,
                Config.BULL * Config.COW,
                Config.CAT * Config.TIGER,
                Config.DOG * Config.WOLF,
                Config.GOAT * Config.SHEEP,
                Config.KANGAROO * Config.KOALA
                ]

        self.SPECIES_DIAMOND = [
                Config.DEER * Config.HORSE,
                Config.HAMSTER * Config.SQUIRREL,
                Config.HAMSTER * Config.MOUSE,
                Config.MOUSE * Config.SQUIRREL
                ]
        #NOTE:
        # same species also get the diamond

        self.SPECIES_CROSS = [
                Config.CAT * Config.MOUSE,
                Config.CAT * Config.HAMSTER,
                Config.DOG * Config.GORILLA,
                Config.DOG * Config.MONKEY,
                Config.SHEEP * Config.WOLF
                ]

        #All other combos get club

        self.SIGN_CROSS = [Config.GROUP_1 * Config.GROUP_4, Config.GROUP_2 * Config.GROUP_3]

        self.GOOD = 1
        self.BAD = -1
        self.AVERAGE = 0

    def __repr__(self):
        return "compatibility object" 

    def personalityCompatibility(self,p1, p2):
        '''
            personality symbol is stored as a character in a jagged 2d array to represent a symmetrical 2d array.
            get symbol by referencing the jagged array using the larger value for the first dimension, and smaller for second.
        '''

        maxPersonality = max(p1, p2)
        minPersonality = min(p1, p2)

        compatibility = self.PERSONALITY_COMPATABILITY[maxPersonality][minPersonality]

        return compatibility

    def speciesCompatibility(self, s1, s2):
        '''
           species are stored as prime numbers, multiply them to get their combination hash.
           Then compare this number to the groupings as provided in the nookipedia webpage
        '''
        compatibilityHash = s1 * s2
        if s1 == s2 or compatibilityHash in self.SPECIES_DIAMOND:
            compatibility = Config.DIAMOND
        elif compatibilityHash in self.SPECIES_HEART:
            compatibility = Config.HEART
        elif compatibilityHash in self.SPECIES_CROSS:
            compatibility = Config.CROSS
        else:
            compatibility = Config.CLUB

        return compatibility

    def signCompatibility(self, s1, s2):
        '''
            sign group is stored as prime numbers, multiply them to get their combination hash.
            Then compare this number ot the grou[ings as provided in the nookipedia webpage
        '''
        compatibilityHash = s1 * s2

        if s1 == s2:
            compatibility = Config.HEART
        elif compatibilityHash in self.SIGN_CROSS:
            compatibility = Config.CROSS
        else:
            compatibility = Config.DIAMOND

        return compatibility

    def calculate(self, v1, v2):
        compatibilityArray = [self.personalityCompatibility(v1.personality, v2.personality),
                self.speciesCompatibility(v1.species, v2.species),
                self.signCompatibility(v1.sign,v2.sign)]

        if compatibilityArray.count(Config.HEART) >= 2 or \
                compatibilityArray == [Config.HEART, Config.DIAMOND, Config.CLUB] or \
                compatibilityArray == [Config.HEART, Config.DIAMOND, Config.DIAMOND]:
            return self.GOOD
        elif compatibilityArray.count(Config.CROSS) >= 2:
            return self.BAD
        else:
            return self.AVERAGE

    def groupScore(self, v):
        runningScore = 0
        for i in range(len(v)):
            for j in range(i):
                runningScore = runningScore + self.calculate(v[i],v[j])
