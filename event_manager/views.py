from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from event_manager.models import EventDb
from event_manager.serializers import *
from rest_framework import authentication, permissions

# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        form_data = request.data
        s_instance = UserSerializer(data= form_data)
        if s_instance.is_valid():
            s_instance.save()
            return Response({"message":"user registration successfull!"}, status=201)
        return Response(s_instance.errors)

class UserListView(APIView):
    def get(self, request):
        qs = User.objects.all()
        s_instance = UserSerializer(qs, many= True)
        return Response(data= s_instance.data)

class UserRetreiveDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(User, id= pk)
        s_instance = UserSerializer(qs)
        return Response(data= s_instance.data)

    def delete(self, request, pk):
        qs = get_object_or_404(User, id= pk)
        qs.delete()
        return Response(data= {"message": "User Deleted Successfully!"})

class EventListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(slef, request):
        events = EventDb.objects.filter(created_by= request.user)
        s_instance = EventSerialiazer(events, many= True)
        return Response(data= s_instance.data)

    def post(self, request):
        form_data = request.data
        s_instance = EventSerialiazer(data= form_data)
        if s_instance.is_valid():
            s_instance.save(created_by= request.user)
            return Response(data= {"message": "Event Created Successfully!",
                                   "your event details":s_instance.data}, status= 201)
        else:
            return Response(data= s_instance.errors, status= 400)

class EventRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        event_object = get_object_or_404(EventDb, id=pk)
        if event_object.created_by == request.user:
            s_instance = EventSerialiazer(event_object)
            return Response(data=s_instance.data)
        else:
            raise serializers.ValidationError("Access Denied")

    def put(self, request, pk):
        event_obj = get_object_or_404(EventDb, id=pk)
        if event_obj.created_by != request.user:
            raise serializers.ValidationError("Access Denied")       
        form_data = request.data
        s_instance = EventSerialiazer(data=form_data, instance=event_obj)
        if s_instance.is_valid():
            s_instance.save()
            return Response(data= {"message": "Updated Successfully!",
                                   "your event details":s_instance.data})
        else:
            return Response(data= s_instance.errors)

    def delete(self, request, pk):
        event_obj = get_object_or_404(EventDb, id=pk)
        if event_obj.created_by != request.user:
            raise serializers.ValidationError("Access Denied")     
        event_obj.delete()
        return Response(data= {"message":"Event Deleted!"})