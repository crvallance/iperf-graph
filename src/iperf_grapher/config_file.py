import pathlib
import tomli
from typing import Type

class Config():
    def __init__(self, config_file: Type[pathlib.Path] = None):
        self.__config = config_file
        toml = TomlReader().load(self.__config)
        self.__token_map = TokenMapConfig(toml['token_map'])

class TokenMapConfig():
    def __init__(self, data):
        self.__delimiter = data['delimiter']
    
    @property
    def Delimiter(self):
        return(self.__delimiter)

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