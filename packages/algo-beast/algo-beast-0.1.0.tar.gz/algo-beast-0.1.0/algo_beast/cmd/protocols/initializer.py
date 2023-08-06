from typing import Protocol


class Initializer(Protocol):
  initialized: bool
  current_directory: str
  current_working_directory: str
  home_directory: str
  package_stubs_directory: str
  user_config_directory: str
  package_config_directory: str
  user_config_file: str
  package_config_file: str
