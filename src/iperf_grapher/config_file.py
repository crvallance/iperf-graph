import pathlib
import tomli
from typing import Type

class Config():
    def __init__(self, config_file: Type[pathlib.Path] = None):
        self.__config = config_file
        toml = TomlReader().load(self.__config)
        self.__tokens = TokenMapConfig(toml)

class TokenMapConfig():
    def __init__(self, data):
        self.__delimiter = data['filename_parsing']['delimiter']
        self.__label_order = data['legend']['label_order']
        self.__tokens = data['filename_parsing']['tokens']
    
    @property
    def delimiter(self):
        return(self.__delimiter)
    
    @property
    def label_order(self):
        return(self.__label_order)

    @property
    def tokens(self):
        return(self.__tokens)


class TomlReader():
    def load(self, config_file):
        try:
            with open(config_file, "rb") as f:
                try:
                    toml_dict = tomli.load(f)
                    return(toml_dict)
                except tomli.TOMLDecodeError:
                    print("TOML File is not valid")
                    raise
        except FileNotFoundError as err:
            print(f'{err}')
            raise