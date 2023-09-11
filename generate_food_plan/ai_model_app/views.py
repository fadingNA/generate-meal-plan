from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PlanGenerationSerializer
import logging
import os
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from django.conf import settings
from .secret_key import APIKEY
import openai
import tiktoken

openai.api_key = APIKEY
os.environ["OPENAI_API_KEY"] = APIKEY
logger = logging.getLogger(__name__)

data_path = os.path.join(
    settings.BASE_DIR, 'ai_model_app', 'llms_model', 'data')
# Create your views here.


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
        model_name=model_name, model_kwargs={'device': 'cuda'}, encode_kwargs=encode_kwargs)
    
    persist_directory = 'db'
    embedding = model_norm
    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
    retriever = vectordb.as_retriever(search_k={"k":5})
    return retriever
    



@api_view(['POST'])
def generate_plan(request):
    logger.info(f"Request: {request.data}")
    input_data = request.data['input_data']
    # Get LLMS function here.
    texts = load_document()
    huggingface_embedding = embeddings_model(texts)
    qa_chain = load_qa_chain(OpenAI(temperature=0.5), chain_type="stuff")
    qa = RetrievalQA(
        combine_documents_chain=qa_chain, retriever=huggingface_embedding,return_source_documents=True)
    _llms_output = qa.run(input_data)
    #generated_plans = retrieve_answer(texts, input_data)
    serializer = PlanGenerationSerializer(data={
        'input_data': input_data,
        'generated_plans': _llms_output
    })

    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
