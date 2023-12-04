import requests
import json

class FileInfo:
    

    def get_dict_from_file(filename):
        with open(filename, 'r') as file:
            fileinfo_dict = json.load(  file)
        return fileinfo_dict
    
    def get_file_from_dict(dictname, new_file):
        with open(new_file, 'w') as file:
            json.dump(dictname, file)
        

    