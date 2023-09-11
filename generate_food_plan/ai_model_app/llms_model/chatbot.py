import os
from langchain.document_loaders import TextLoader, WebBaseLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


def load_document():
    loader = DirectoryLoader('./data', glob="**/*.csv")
    data = loader.load()
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_spliter.split_documents(data)
    return texts

def retrieve_answer(texts,query):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(texts, embeddings)
    qa_chain = load_qa_chain(OpenAI(temperature=0.5), chain_type="stuff")
    qa = RetrievalQA(
        combine_documents_chain=qa_chain, retriever=vectordb.as_retriever())
    
    output = qa.run(query)
    return output
    
