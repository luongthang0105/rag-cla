import click 
from newbot_command import *
from usebot_command import *
from addfile_command import *
@click.group
def allCommands():
	pass

allCommands.add_command(newBot)
allCommands.add_command(useBot)
allCommands.add_command(addFile)

if __name__ == "__main__":
	allCommands()
