"""
file module - handles file operations
mainly ini/json file storage of dictionaries
ver. 2019-01-28
"""
from os import getcwd #, path #import os
try:
    from os import path
except:
    print('warning, path module not imported')
import json
import io


class ini:
    """
    class for ini file operations
    """
    def __init__(self):
        self.version = '0.1'
        self.host = ''
        self.port = 0

    def read(self, file1):
        """
        reads ini file, returns dictionary
        """
        dir_path = path.dirname(path.realpath(__file__))
        print('working directory: ', dir_path)
        print('config file location: ', file1)
        try:
            with io.open(file1) as data_file:#with io.open(path.join(dir_path, file1)) as data_file:
                data_loaded = json.load(data_file)
        except:
            data_loaded = {'host': '10.10.10.1', 'port': 8003}          #returns default
            print('error reading file, using default: ', data_loaded)
        print(data_loaded)
        return data_loaded

    def write(self, file1, data):
        """
        writes dictionary into the file
        """
        str1 = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        print(str1)
        dir_path = path.dirname(path.realpath(__file__))
        file1 = io.open(path.join(dir_path, file1), 'w', encoding='utf8')
        file1.write(str1)
        file1.close()


class Ini2:
    def read(self, file1):
        """
        reads ini file, returns dictionary
        """
        dir_path = path.dirname(path.realpath(__file__))
        # print('working directory: ', dir_path)
        print('config file location: ', file1)
        try:
            with io.open(file1) as data_file:#with io.open(path.join(dir_path, file1)) as data_file:
                data_loaded = json.load(data_file)
        except:
            data_loaded = {}          #returns default
            print('error reading file, returning default: ', data_loaded)
        # print('data loaded: ', data_loaded)
        return data_loaded

    def write(self, file1, data):
        """
        writes dictionary into the file
        """
        str1 = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=True)
        # print('data to write: ' + str1)
        print('writing file: ' + file1)
        file_1 = io.open(file1, 'w', encoding='utf8')
        file_1.write(str1)
        file_1.close()


class uini:
    'microptyhon 1.9.4 ini file operations implementation'
    def read(self, file1):
        'reads json file, returns dictionary'
        self.data_dir = getcwd()
        print('datadir: ', self.data_dir)
        self.file = io.open(self.data_dir + file1)
        #self.file_data = self.file.read()
        #self.json_data = json.loads(self.file_data)
        self.json_data = json.load(self.file)
        self.file.close()
        print('json data: ', self.json_data)
        return self.json_data


def test():
    ini = Ini2()
    data = ini.read('C:\\Users\\pkrssak\\AppData\\Roaming\\dqi_proj_accept\\Sample project_0008.json')
    print('loaded data: ', data)


if __name__ == '__main__':
    test()