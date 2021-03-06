import os
import time
from typing import Optional, Union

import yaml


def ensure_exists(dir_to_validate) -> str:
    """Ensure directory exists"""
    if not os.path.exists(dir_to_validate):
        os.makedirs(dir_to_validate)
    return dir_to_validate


def current_milli_time():
    """ "Get current time in milliseconds"""
    return round(time.time() * 1000)


class FileSystem:
    @staticmethod
    def __get_base_dir():
        """At most all application packages are just one level deep"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, "..")

    @staticmethod
    def __get_config_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, "config")

    @staticmethod
    def get_plugins_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, "plugins")

    @staticmethod
    def get_share_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.abspath(os.path.join(base_dir, "share"))

    @staticmethod
    def load_configuration(name: str = "marie.yaml", config_directory: Optional[str] = None) -> dict:
        if config_directory is None:
            config_directory = FileSystem.__get_config_directory()
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data
