from django.shortcuts import  redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PlanGenerationSerializer
import logging
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from django.conf import settings
from .secret_key import APIKEY
import openai
import tiktoken
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from .utils import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import RegisterForm


openai.api_key = APIKEY
os.environ["OPENAI_API_KEY"] = APIKEY
logger = logging.getLogger(__name__)

data_path = os.path.join(
    settings.BASE_DIR, 'ai_model_app', 'llms_model', 'data')
# Create your views here.


def home(request):
    return render(request, 'main/home.html')

@api_view(['POST'])
@permission_classes([IsAdminUser])
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


@api_view(['POST'])
def create_user_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=400)
    
    # Check if the user already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully!'}, status=201)


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
        
