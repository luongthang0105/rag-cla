import click
from newbot_command import *
from langchain.embeddings import HuggingFaceEmbeddings

INPUT_TYPES = {
	"doc": "pdf",
	"web": "url"
}
@click.command()
@click.option("-n", "--name", prompt = 'Enter your chat bot name: ', help = "Name of the chat bot")
@click.option("-t", "--filetype", "fileType", prompt = 'What kind of file does your chatbot refer to ? (doc/web)', help = 'Type of files for context', type = click.Choice(INPUT_TYPES.keys()))
@click.option("--path", prompt = False, type = click.Path(exists = False), help = 'Path of given document/image')
@click.option("--url", prompt = False, help = 'Url of given web page')

def addFile(name, fileType, path, url):
	"""
		Add more files to current vectorstore of the given chatbot
	"""

	validUrlOrPath(fileType, path, url)

	print(f'Gimme a sec...')
	persistentDir = "bots/" + name + "/vectorstore/"
	embeddings = HuggingFaceEmbeddings()

	vectorstore = Chroma(persist_directory=persistentDir, embedding_function=embeddings)

	if fileType == 'web':
		loader = WebBaseLoader(url)
	elif fileType == 'doc':
		loader = WebBaseLoader(path)

	data = loader.load()

	text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
	all_splits = text_splitter.split_documents(data)

	vectorstore.add_documents(all_splits)

	print(f"Files added to chatbot '{name}' vectorstore successfully!")