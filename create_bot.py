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
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQAWithSourcesChain

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

	vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)

	jina_api_key = os.environ['JINA_API_KEY']
	chat = JinaChat(temperature=0, jinachat_api_key=jina_api_key)

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

	botSavePath = "bots/" + name + '.json'	
	finalChain.save(botSavePath)

	return finalChain