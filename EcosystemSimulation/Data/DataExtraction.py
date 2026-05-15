import csv
from pathlib import Path
import io
import pandas as pd
import urllib.request
import zipfile
class DataExtraction:
    def validate(self):
        pass

    def extract(self):
        pass

# excel extraction
#reads data and turns into data python can read
class ExcelDataExtraction(DataExtraction):
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def extract(self):
        self.validate()

        with self.file_path.open("r", encoding="utf-8") as f:
            text = f.read()

        try:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(text.splitlines()[0])
            delimiter = dialect.delimiter
        except Exception:
            delimiter = "\t"

        reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
        return [dict(row) for row in reader]



# site extraction
#Grab
class SiteDataExtraction(DataExtraction):
    def __init__(self, url):
        self.url = url

    def extractMammalData(self):
        df = pd.read_csv(self.url, sep='\t', na_values=-999)

        dfSelected = df.loc[:, [
            # ID
            "MSW93_Order",
            "MSW93_Family",
            "MSW93_Genus",
            "MSW93_Species",
            "MSW93_Binomial",

            # body
            "5-1_AdultBodyMass_g",
            "13-1_AdultHeadBodyLen_mm",

            # reproduction
            "3-1_AgeatFirstBirth_d",  
            "15-1_LitterSize",
            "14-1_InterBirthInterval_d",
            "7-1_DispersalAge_d",
            "25-1_WeaningAge_d",

            # lifespan
            "17-1_MaxLongevity_m",

            # ecology / predator–prey
            "6-2_TrophicLevel",

            # home range / movement
            "22-1_HomeRange_km2",

            #habitat
            "12-2_Terrestriality",
        ]]

        dfSelected = dfSelected.rename(columns={
            "MSW93_Order": "order",
            "MSW93_Family": "family",
            "MSW93_Genus": "genus",
            "MSW93_Species": "species_short",
            "MSW93_Binomial": "species",

            "5-1_AdultBodyMass_g": "adult_mass_g",
            "13-1_AdultHeadBodyLen_mm": "body_length_mm",

            "3-1_AgeatFirstBirth_d": "age_first_birth_d",  
            "15-1_LitterSize": "litter_size",
            "14-1_InterBirthInterval_d": "interbirth_interval_d",
            "7-1_DispersalAge_d": "dispersal_age_d",
            "25-1_WeaningAge_d": "weaning_age_d",

            "17-1_MaxLongevity_m": "max_longevity_m",

            "6-2_TrophicLevel": "trophic_level",
            "22-1_HomeRange_km2": "home_range_km2",

            "12-2_Terrestriality": "terrestriality",
        })

        # save CSV 
        outputPath = "mammalAnimals.csv"
        dfSelected.to_csv(outputPath, index=False)
        print(f"Saved: {outputPath}")


        return dfSelected
    


    

    


def extractAll():
    # Mammal
    Mammal = SiteDataExtraction(
        "https://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR93_Aug2008.txt"
    )
    Mammal.extractMammalData()


    
import os

def ensureMammalCSV(
    url="https://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR93_Aug2008.txt",
    outputPath="mammalAnimals.csv",
):
    """
    Make sure the main mammal CSV exists. if it doesnt then call SiteDataExtraction.extractMammalData() to create it
    and return the path to the CSV.
    """
    if os.path.exists(outputPath):
        return outputPath

    mammalExtractor = SiteDataExtraction(url)
    mammalExtractor.extractMammalData()
    return outputPath

def loadMammalTraitRow(csvPath = "mammalAnimals.csv"):

    path = Path(csvPath)
    from Data.DataExtraction import ensureMammalCSV
    ensureMammalCSV()
    if not path.exists():
        raise FileNotFoundError(f"Could not find {csvPath} even after ensureMammalCSV()")
    

    rows = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows



if __name__ == "__main__":
    extractAll()
        



