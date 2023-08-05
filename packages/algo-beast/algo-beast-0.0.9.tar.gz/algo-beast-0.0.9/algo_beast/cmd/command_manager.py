from algo_beast.cmd.commands.create_project import CreateProject
from algo_beast.cmd.commands.list import List


class CommandManager:
  commands = {
    "local": {
      "init": CreateProject,
      "list": CreateProject,
      "create": CreateProject,
      "delete": CreateProject,
      "run": CreateProject,
    },
    "cloud": {
      "push": CreateProject,
      "pull": CreateProject,
    }
  }

  @staticmethod
  def detect_environment(argv: list):
    try:
      if argv[0] not in ["local", "cloud"]:
        argv.insert(0, "local")
      environment = argv[0]
    except IndexError:
      environment = "local"

    try:
      command = CommandManager.commands[environment][argv[1]]
    except KeyError:
      raise Exception("Invalid command")
    except IndexError:
      command = List

    try:
      arguments = argv[2:] if len(argv) > 2 else []
    except IndexError:
      arguments = []
    
    return environment, command, arguments

  @staticmethod
  def manage(argv):
    environment, command, arguments = CommandManager.detect_environment(argv)
    instance = command(environment, arguments)
    info = instance.run()
    print(info)