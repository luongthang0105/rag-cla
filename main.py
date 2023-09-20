import click 
from newbot_command import *

@click.group
def allCommands():
	pass

allCommands.add_command(newBot)
if __name__ == "__main__":
	allCommands()
