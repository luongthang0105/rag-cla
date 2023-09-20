import click
import os
import validators
from create_bot import *
import keyboard

def validateUrl(url):
	if validators.url(url) == True:
		return True
	return False

def validUrlOrPath(fileType, path, url):
	if fileType in ['doc']:
		if path == None:
			raise click.UsageError(message = "Valid path should be provided for document/image")
		else:
			if not os.path.isfile(path):
				raise click.UsageError(message = "Can't find a file with given path")
	
	if fileType == 'web':
		if url == None:
			raise click.UsageError(message = "Valid url should be provided for document/image")
		else:
			if not validateUrl(url):
				raise click.BadParameter('must be a valid url')

INPUT_TYPES = {
	"doc": "pdf",
	"web": "url"
}

@click.command()
@click.option("-n", "--name", prompt = 'Enter your chat bot name: ', help = "Name of the chat bot")
@click.option("-t", "--filetype", "fileType", prompt = 'What kind of file does your chatbot refer to ? (document/image/web)', help = 'Type of files for context', type = click.Choice(INPUT_TYPES.keys()))
@click.option("--path", prompt = False, type = click.Path(exists = False), help = 'Path of given document/image')
@click.option("--url", prompt = False, help = 'Url of given web page')

def newBot(name, fileType, path, url):
	"""
	Create an instance of chatbot with the given name. \n
	If the given context for chatbot is document or image, then a PATH should be provided.\n
	If a web page is given as context, then an URL should be provided.
	"""
	print(f'Creating a new chatbot called "{name}"... ')
	
	# print(name, fileType, path, url)

	validUrlOrPath(fileType, path, url)

	chatBot = createNewBot(name, fileType, path, url)

	print(f'Bot "{name}" created successfully!')

	print(f'Ask chatbot {name} something or type "esc" to end session: ')

	while True:
		query = input()
		if query == 'esc': break
		print()
		print(f"Waiting for chatbot's response...")
		# response = chatBot.run(query)
		# print(f"""Response: {response['answer']}""")
		answer = chatBot(query)['answer']
		print(f"""{answer}""")

		print(f"Your next query: ")

	print('Conversation ended!')

