from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from event_manager.serializers import UserSerializer

# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        form_data = request.data
        s_instance = UserSerializer(data= form_data)
        if s_instance.is_valid():
            s_instance.save()
            return Response({"message":"user registration successfull!"}, status=201)
        return Response(s_instance.errors)

