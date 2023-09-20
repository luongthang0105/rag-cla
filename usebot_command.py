import click
from langchain.chains import load_chain
import os
import json 
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

@click.command()
@click.option('-n', '--name', prompt = 'Enter your chatbot name: ', help = 'Name of the chatbot')
def useBot(name):
	"""
		Use the chatbot with given name.
	"""
	botPath 	  = "bots/" + name + '/' + name + '.json'

	if not os.path.isfile(botPath):
		raise click.UsageError(message = "Can't find a chatbot with given name") 

	# with open(retrieverPath) as f:
	# 	retrieverDict = json.load(f)
	# print(retrieverDict)
	persistentDir = "bots/" + name + '/vectorstore/'
	embeddings = HuggingFaceEmbeddings()

	vectorstore = Chroma(persist_directory=persistentDir, embedding_function=embeddings)
	retriever = vectorstore.as_retriever()

	chatBot = load_chain(botPath, retriever = retriever)

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