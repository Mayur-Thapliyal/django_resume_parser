from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from ITresumeParser.utils import *
from django.core.files.base                             import ContentFile
from django.core.files.storage                          import default_storage
import os
from ITresumeParser.settings import MEDIA_ROOT
from .serializers import *
from rest_framework import status
from shutil import rmtree
# Create your views here.

class AppView(ViewSet):
    parser_classes=[MultiPartParser]

    @action(methods=['POST'],detail=False)
    @swagger_auto_schema(operation_description="To get Parse and get Data from resume provided in docx and pdf format",
    operation_summary="get data from rsume",
    request_body=FileSerializer,
    tags=["Parsing"])
    def demo_api(self,request):
        try:
            serializers_obj = FileSerializer(data=request.data)
            if serializers_obj.is_valid(raise_exception=True):

                file                        =           request.FILES['file_to_upload']
                if ".pdf" in str(file):
                    file_extention = ".pdf"
                elif ".docx" in str(file):
                    file_extention = ".docx"
                else :
                    return Response({"message" :"Invalid file format","status":status.HTTP_400_BAD_REQUEST})

                file_name                   =           str(file) [0:str(file).rfind(file_extention)]
                print(file_name)
                path                        =           default_storage.save('/'.join([str(file_name),str(file)]), ContentFile(file.read()))
                filepath                    =           os.path.join(MEDIA_ROOT, path)
                text = extract_text(file_path = filepath)
                nlp = spacy.load('en_core_web_sm')
                doc=nlp(text=text)
                noun_chunks = doc.noun_chunks
                matcher = Matcher(nlp.vocab)
                data =exteact_details_from_resume(text = text, noun_chunks = noun_chunks, matcher= matcher, nlp = nlp)
                rmtree(path=MEDIA_ROOT+f'/{file_name}')
                return Response({"message" :"Successful","data" :data,"status":status.HTTP_200_OK})
        except Exception as e:
            return Response({"message" :"Something went wrong","dbug_message" :str(e),"status":status.HTTP_400_BAD_REQUEST})
        