class DataStore:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def add_entries(self, entries):
        # add to disk  
        pass

    def process(self):
        # process / clean the stored data before saving
        return self.data

    def save(self, file_path):
        # save processed data to excel/ csv file
        pass