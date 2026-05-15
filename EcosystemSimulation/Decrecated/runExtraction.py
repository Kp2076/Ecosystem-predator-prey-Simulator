# data/runExtraction.py
from DataExtraction import DataExtraction, ExcelDataExtraction, SiteDataExtraction
from EcosystemSimulation.Decrecated.DataStore import DataStore

def main():
    # extract from Excel
    excel_extractor = ExcelDataExtraction("xlsx")
    excel_data = excel_extractor.extract()

    # extract from site
    site_extractor = SiteDataExtraction("link")
    site_data = site_extractor.extract()

    # Store and process
    store = DataStore()
    store.add_entries(excel_data)
    store.add_entries(site_data)
    processed = store.process()

    # Save processed data
    store.save()

if __name__ == "__main__":
    main()
