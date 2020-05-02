import Config
from bs4 import BeautifulSoup
import requests
import pandas as pd

#pull data from this webpage:
#http://nookipedia.com/wiki/List_of_villagers

class Spider():
    def __init__(self):
        self.BASE_URL = "http://nookipedia.com/"
        self.LIST_URL = "wiki/List_of_villagers"
        self.PARSER = "html.parser"
        self.NAME = "Name"

    def main(self):
        if Config.VERBOSE:
            print("Opening the villager list now")

        #Open up the main url
        req = requests.get(self.BASE_URL + self.LIST_URL)
        villagerListSoup = BeautifulSoup(req.text, self.PARSER)

        #Create a new pandas dataframe

        villagerFrame = pd.DataFrame(columns = [Config.NAME, Config.PERSONALITY, Config.SPECIES, Config.STAR_SIGN])

        #Iterate thru rows of the villager list table
        tableRow = villagerListSoup.find_all("tr")
        for i in range(2, len(tableRow)-1):
            #Skip the headers, and the last row that allows you to go back to top
            ths = tableRow[i].find_all("th")
            tds = tableRow[i].find_all("td")

            #check whether this villager is in ACNH
            inACNH = not tds[11].find("a") is None

            if inACNH:
                nameAnchorTag = ths[1].find("a")

                #Follow the link
                req = requests.get(self.BASE_URL + nameAnchorTag["href"])
                villagerSoup = BeautifulSoup(req.text, self.PARSER)

                #Get the name
                name = nameAnchorTag.string
                #Get the personality
                personality = tds[3].find("a").string
                #Get the species
                species = tds[1].find("a").string
                #Get the sign
                sign = villagerSoup.find(id="Infobox-villager-starsign").find("a")["title"]

                #Insert this data into the dataframe
                villagerFrame = villagerFrame.append({Config.NAME:name,
                                                        Config.PERSONALITY:personality,
                                                        Config.SPECIES:species,
                                                        Config.STAR_SIGN:sign
                                                        }, ignore_index = True)
                if Config.DEBUG:
                    print(str(name) + "," + str(personality) + "," + str(species) + "," + str(sign))


        if Config.VERBOSE:
            print("Done crawling through villagers")
        villagerFrame.to_csv(Config.VILLAGERS_DATA_SOURCE, index=False)


if __name__ == "__main__":
    spider = Spider()
    spider.main()
