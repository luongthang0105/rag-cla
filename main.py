import click 
from newbot_command import *
from usebot_command import *
@click.group
def allCommands():
	pass

allCommands.add_command(newBot)
allCommands.add_command(useBot)

if __name__ == "__main__":
	allCommands()
