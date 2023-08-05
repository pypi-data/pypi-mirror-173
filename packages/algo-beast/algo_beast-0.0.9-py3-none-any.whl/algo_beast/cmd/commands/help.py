class Help:
  def __init__(self, environment, arguments) -> str:
    self.environment = environment
    self.arguments = arguments
  
  def run(self):
    print(self.environment, self.arguments)