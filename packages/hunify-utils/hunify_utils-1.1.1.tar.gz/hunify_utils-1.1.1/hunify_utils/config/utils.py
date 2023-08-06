import os
import json
import logging
from configparser import ConfigParser, Error as CPError

from .errors import ParseError


def get_file_extension(file_path: str) -> str:
    filepath, extension = os.path.splitext(file_path)
    extension = extension[1::]  # trimming starting .
    return extension


def save_dict_as_json(file_path: str, dictionary: dict):
    try:
        with open(file_path, 'w') as configfile:
            json.dump(dictionary, configfile, indent=4)
    except IOError as e:
        logging.error(f"Error creating config file: {e.message}")
        exit(-1)


def save_dict_as_ini(file_path: str, dictionary: dict):
    try:
        config_out = ConfigParser()
        for k, v in list(dictionary.items()):
            if not isinstance(v, dict):
                if "default" not in dictionary.keys():
                    dictionary["default"] = {}
                dictionary["default"][k] = dictionary.pop(k)

        config_out.read_dict(dictionary)
        with open(file_path, 'w') as configfile:
            config_out.write(configfile)
    except CPError as e:
        logging.error(f"Error creating config.py file: {e.message}")


def load_dict_from_ini(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise ParseError(f"File {file_path} does not exist")
    try:
        config_in = ConfigParser()
        config_in.read(file_path)
        logging.debug("Config file loaded")
        config = {s: dict(config_in.items(s)) for s in config_in.sections()}
        return config
    except CPError as e:
        logging.error(f"Error loading file {file_path}: {e.message}")
        raise e


def load_dict_from_json(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise ParseError(f"File {file_path} does not exist")
    with open(file_path, 'r') as config_file:
        d = json.load(config_file)
        return d
