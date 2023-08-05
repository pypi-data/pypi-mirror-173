class CreateProject:
  def __init__(self, environment, arguments) -> str:
    self.environment = environment
    self.arguments = arguments
  
  def run(self):
    print("create project", self.environment, self.arguments)