from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os
from langchain.chat_models import JinaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatAnyscale
from langchain.llms import AI21

import json
# create a new instance of chatbot and saves it as a JSON file
def createNewBot(name, fileType, path, url):
	loader = None
	
	if fileType == 'web':
		loader = WebBaseLoader(url)
	elif fileType == 'doc':
		loader = PyPDFLoader(path)

	data = loader.load()

	text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
	all_splits = text_splitter.split_documents(data)
	
	embeddings = HuggingFaceEmbeddings()

	persistentDir = "bots/" + name + "/vectorstore/" 
	vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory=persistentDir)
	# print(vectorstore)
	# jina_api_key = os.environ['JINA_API_KEY']
	# chat = JinaChat(temperature=0, jinachat_api_key=jina_api_key)

	# chat = ChatAnyscale(model_name='meta-llama/Llama-2-7b-chat-hf', temperature=1.0, anyscale_api_key=os.environ["ANYSCALE_API_KEY"])
	chat = AI21(ai21_api_key=os.getenv("AI21_API_KEY"))
	# memory = ConversationSummaryMemory(llm=chat,memory_key="chat_history",return_messages=True)

	retriever = vectorstore.as_retriever()

	template = (
    r"""You are a helpful English speaking assistant. Use the following pieces of context to answer the users question. If you cannot find the answer from the pieces of context, just say that you don't know, don't try to make up an answer. 
	---------------- 
	{context}
	"""
	)
	system_message_prompt = SystemMessagePromptTemplate.from_template(template)
	human_template = "{question}"
	human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

	chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
	)

	# finalChain = ConversationalRetrievalChain.from_llm(chat, retriever=retriever, memory = memory, combine_docs_chain_kwargs={'prompt': chat_prompt})
	finalChain = RetrievalQAWithSourcesChain.from_chain_type(chat, retriever=retriever)

	# print(finalChain.retriever)
	# SAVING DOESNT WORK OUT BECAUSE LANGCHAIN HAS YET TO SUPPORT THIS
	chainSaveFolder = "bots/" + name + '/'
	
	botSavePath = chainSaveFolder + name + '.json'
	finalChain.save(botSavePath)

	# retrieverSavePath = chainSaveFolder + name + '_retriever.json'
	# with open(retrieverSavePath, "w") as f:
	# 	# json.dump(finalChain.retriever.to_json(), f, indent = 2)
	# 	json.dump(vectorstore, f, indent = 2)

	return finalChain