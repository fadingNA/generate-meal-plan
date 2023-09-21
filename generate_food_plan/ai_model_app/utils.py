from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


def load_document():
    loader = DirectoryLoader(data_path, glob="**/*.csv",
                             show_progress=True, use_multithreading=True)
    data = loader.load()
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    texts = text_spliter.split_documents(data)
    return texts


def retrieve_answer(texts, query):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(texts, embeddings)
    
    #output = qa.run(query)
    output = []
    return output


def embeddings_model(texts):
    model_name = 'BAAI/bge-base-en'
    encode_kwargs = {
        'normalize_embeddings': True,
    }
    model_norm = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs={'device': 'cpu'}, encode_kwargs=encode_kwargs)
    
    persist_directory = 'db'
    embedding = model_norm
    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
    retriever = vectordb.as_retriever(search_k={"k":5})
    return retriever
    
