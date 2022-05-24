import pathlib
import tomli
from typing import Type

class Config():
    def __init__(self, config_file: Type[pathlib.Path] = None):
        self.config_file = config_file
        try:
            self.__load_config()
        except:
            print('Bare except is bad...')

    def __load_config(self) -> dict:
        try:
            with open(self.config_file, "rb") as f:
                try:
                    toml_dict = tomli.load(f)
                    self.toml_dict = toml_dict
                except tomli.TOMLDecodeError:
                    print("TOML File is not valid")
                    raise
        except FileNotFoundError as err:
            print(f'{err}')
            raise
        # return(toml_dict)
    
    def get_settings(self):
        return(self.toml_dict)

