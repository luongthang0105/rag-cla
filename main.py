import click

@click.group
def allCommands():
	pass

import validators

def validateUrl(ctx, param, value):
	print(ctx.command)
	if validators.url(value) == True:
		return value
	else:
		raise click.BadParameter('must be a valid url')

INPUT_TYPES = {
	"doc": "pdf",
	"img": "png",
	"web": "url"
}

@click.command()
@click.option("-n", "--name", prompt = 'Enter your chat bot name: ', help = "Name of the chat bot")
@click.option("-t", "--filetype", "fileType", prompt = 'What kind of file does your chatbot refer to ? (document/image/web)', help = 'Type of files for context', type = click.Choice(INPUT_TYPES.keys()))
@click.option("--path", prompt = False, type = click.Path(exists = True), help = 'Path of given document/image')
@click.option("--url", prompt = False, help = 'Url of given web page', callback = validateUrl)

def newBot(name, fileType, path, url):
	"""
	Create an instance of chatbot with the given name. \n
	If the given context for chatbot is document or image, then a PATH should be provided.\n
	If a web page is given as context, then an URL should be provided.
	"""
	print(f'Creating a new chatbot called "{name}"... ')
	
	# print(name, fileType, path, url)
	
	if fileType in ['doc', 'img']:
		if path == None:
			raise click.UsageError(message = "Valid path should be provided for document/image")
	
	if fileType == 'web':
		if url == None:
			raise click.UsageError(message = "Valid url should be provided for document/image")
	

allCommands.add_command(newBot)
if __name__ == "__main__":
	allCommands()
