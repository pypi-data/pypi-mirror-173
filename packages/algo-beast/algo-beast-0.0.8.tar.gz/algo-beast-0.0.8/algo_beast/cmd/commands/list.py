class List:
  def __init__(self, environment, arguments) -> str:
    self.environment = environment
    self.arguments = arguments
  
  def run(self):
    if self.environment == "local":
      return self.list_local_commands()
    else:
      return self.list_cloud_commands()
  
  def list_local_commands(self):
    command = '\n'
    command += f'algo-beast init                              [Initialize AlgoBeast CLI]'
    command += '\n'
    command += f'algo-beast list            <project_name>    [List all projects]'
    command += '\n'
    command += f'algo-beast create          <project_name>    [Create a project]'
    command += '\n'
    command += f'algo-beast delete          <project_name>    [Delete a project]'
    command += '\n'
    command += f'algo-beast backtest        <project_name>    [Run project in cloud server]'
    command += '\n'
    command += f'algo-beast paper           <project_name>    [Run project in cloud server]'
    command += '\n'
    command += f'algo-beast live            <project_name>    [Run project in cloud server]'
    command += '\n'
    command += '\n'
    command += f'algo-beast cloud pull      <project_name>    [Pull cloud projects]'
    command += '\n'
    command += f'algo-beast cloud push      <project_name>    [Push cloud projects]'
    command += '\n'
    command += f'algo-beast cloud list      <project_name>    [List all projects]'
    command += '\n'
    command += f'algo-beast cloud create    <project_name>    [Create a project]'
    command += '\n'
    command += f'algo-beast cloud delete    <project_name>    [Delete a project]'
    command += '\n'
    command += f'algo-beast cloud backtest  <project_name>    [Run project in cloud server]'
    command += '\n'
    command += f'algo-beast cloud paper     <project_name>    [Run project in cloud server]'
    command += '\n'
    command += f'algo-beast cloud live      <project_name>    [Run project in cloud server]'
    command += '\n'

    return command
  
  def list_cloud_commands(self):
    command = '\n'
    command += f'algo-beast cloud pull      <project_name>    [Pull cloud projects]'
    command += '\n'
    command += f'algo-beast cloud push      <project_name>    [Push cloud projects]'
    command += '\n'
    command += f'algo-beast cloud list      <project_name>    [List all projects]'
    command += '\n'
    command += f'algo-beast cloud create    <project_name>    [Create a project]'
    command += '\n'
    command += f'algo-beast cloud delete    <project_name>    [Delete a project]'
    command += '\n'
    command += f'algo-beast cloud backtest  <project_name>    [Run project in cloud server]'
    command += '\n'
    command += f'algo-beast cloud paper     <project_name>    [Run project in cloud server]'
    command += '\n'
    command += f'algo-beast cloud live      <project_name>    [Run project in cloud server]'
    command += '\n'

    return command
