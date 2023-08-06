import os
import shutil

from algo_beast.cmd.protocols import Initializer


class Initializer(Initializer):
  initialized: bool = False
  current_directory: str = os.path.dirname(__file__)
  current_working_directory: str = os.getcwd()
  home_directory: str = os.path.expanduser('~')
  package_stubs_directory: str = os.path.join(current_directory, "..", "stubs")
  user_config_directory: str = os.path.join(home_directory, ".algo-beast")
  package_config_directory: str = os.path.join(package_stubs_directory, ".algo-beast")
  user_config_file: str = os.path.join(user_config_directory, "config.json")
  package_config_file: str = os.path.join(package_config_directory, "config.json")

  def __init__(self) -> bool:
    self.init()

  def init(self):
    if not os.path.exists(self.user_config_directory):
      os.mkdir(self.user_config_directory)

    if not os.path.exists(self.user_config_file):
      shutil.copy(self.package_config_file, self.user_config_directory)

    self.initialized = os.path.exists(self.user_config_file)
