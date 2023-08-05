from sys import argv

from algo_beast_core.app import App

app = App()
app.add_session(argv)
app.run()
