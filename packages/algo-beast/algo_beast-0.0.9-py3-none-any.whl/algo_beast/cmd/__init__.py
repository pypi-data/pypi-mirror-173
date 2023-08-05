from sys import argv

from algo_beast.cmd.command_manager import CommandManager


def main():
  del argv[0]
  CommandManager.manage(argv)

if __name__ == "__main__":
  main()
