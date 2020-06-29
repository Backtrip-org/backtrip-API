import configparser
import os

from app.main.util.exception.ConfigException import CouldNotReadConfigVariablesException


class ConfigVariables:

    def __init__(self, env: str, config_file_folder: str):
        self.env = env or 'dev'
        self.__config_parser = configparser.ConfigParser()
        config_file_path = os.path.join(config_file_folder, 'config.ini')
        if len(self.__config_parser.read(config_file_path)) != 1:
            raise CouldNotReadConfigVariablesException()

    def get(self, key: str):
        return self.__config_parser[self.env][key]