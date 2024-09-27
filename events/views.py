from email.message import EmailMessage
from django.shortcuts import render
from rest_framework.decorators import APIView,api_view,permission_classes
# Create your views here.
from .serializers import *
from users.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import check_password
from decouple import config
from django.template.loader import render_to_string
import os


class Vote(APIView):
    permission_classes=[AllowAny,]
    def post(self,request):
        try:
            data = request.data
            vote_serializer = VoteSerializer(data = data)
            event = EVENT.objects.get(id=data['event'])
            if event.paid:
                value = float(data['vote']) *float(event.amount)
                event.total_balance = float(event.total_balance) +float(value)
                event.save()

            if vote_serializer.is_valid():
                vote_serializer.save()
                return Response(vote_serializer.data,status.HTTP_201_CREATED)
            else:
                return Response(vote_serializer.errors,status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as E:
            return Response(f'An error occurred {E}',status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def select_prime_contestant_image(request,id):
    
    data = request.data
    ContestanInfoImages.objects.filter(contestant__id=data['contestant']).update(prime_image=False)
    ContestanInfoImages.objects.filter(id=id).update(prime_image=True)
    return Response('Image Status Updated',status.HTTP_202_ACCEPTED)

class ContestantView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    
    def put(self,request,id):
        try:
            contestant_information = ContestantInfo.objects.get(id = id)
        except ContestantInfo.DoesNotExist:
            return Response('Invalid contestant ID passed',status.HTTP_404_NOT_FOUND)
        request_data = request.data
        data = request_data.copy()
        contestant = ContestantSerializer(contestant_information,data = data,partial=True)
        if contestant.is_valid():
            contestant.save()
        if 'deleted_image_1' in data:
            img_1 = ContestanInfoImages.objects.get(id = data['deleted_image_1'])
            img_1.delete()
        if 'deleted_image_2' in data:
            img_2 = ContestanInfoImages.objects.get(id = data['deleted_image_2'])
            img_2.delete()
        if 'deleted_image_3' in data:
            img_3 = ContestanInfoImages.objects.get(id = data['deleted_image_3'])
            img_3.delete()
        if 'deleted_image_4' in data:
            img_4 = ContestanInfoImages.objects.get(id = data['deleted_image_4'])
            img_4.delete()

        data['contestant'] = contestant_information.id
        contestant_image_serializer = ContestantImageSerializers(data = data)
        if contestant_image_serializer.is_valid():
            contestant_image_serializer.save()
        return Response(contestant.data,status.HTTP_201_CREATED)
        
    def delete(self,request,id):
        try:
            user = request.query_params.get('user')
            password = request.query_params.get('password')
            try:
                contestant_information = ContestantInfo.objects.get(id = id)
            except ContestantInfo.DoesNotExist:
                return Response('Invalid contestant ID passed',status.HTTP_404_NOT_FOUND)
            if ((contestant_information.event.event_organizer.id) == int(user) and check_password(password,contestant_information.event.event_organizer.password)):
                contestant_images = ContestanInfoImages.objects.filter(contestant = contestant_information)

                for data in contestant_images:
                    if data.contestantdata_images:
                        if os.path.isfile(data.contestantdata_images.path):
                            os.remove(data.contestantdata_images.path)
                contestant_information.delete()
                return Response(status.HTTP_204_NO_CONTENT)
            else:
                return Response('Invalid credentials for event organizer',status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response(f'An error occurred \n{E}',status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):

        event = request.query_params.get('event',None)

        if event:
            contestant_info =  ContestantInfo.objects.filter(event__id=event)
        else:
            contestant_info =  ContestantInfo.objects.all()


        contestant_serializer = ContestantSerializer(contestant_info,many=True)

        return Response(contestant_serializer.data,status.HTTP_200_OK)
        
    def post(self,request):
        try:
            request_data = request.data
            data = request_data.copy()
            contestant = ContestantSerializer(data = data)
            if contestant.is_valid():
                contestant_data = contestant.save()
            else:
                return Response(contestant.errors,status.HTTP_500_INTERNAL_SERVER_ERROR)
            data['contestant'] = contestant_data.id
            contestant_image_serializer = ContestantImageSerializers(data = data)
            if contestant_image_serializer.is_valid():
                contestant_image_serializer.save()
            return Response(contestant.data,status.HTTP_201_CREATED)
        except Exception as E:
            return Response(f'An error occurred \n {E}',status.HTTP_400_BAD_REQUEST)
        
class EVENTSVIEW(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    def get(self,request):
        user_id = request.query_params.get('user_id',None)
        if user_id:
            try:
                user = USERMODEL.objects.get(id=user_id)
            except USERMODEL.DoesNotExist:
                return Response('Invalid user id',status.HTTP_404_NOT_FOUND)
            
            events =  EVENT.objects.filter(event_organizer = user)
        else:
            events =  EVENT.objects.all()

        event_serializer = EventSerializer(events,many=True)

        return Response(event_serializer.data,status.HTTP_200_OK)
    
    def post(self,request):
        try:
            request_data = request.data

            data = request_data.copy()


            search_event = EVENT.objects.filter(event_code__iexact=str(data["name_of_event"])[0:4])

            if search_event.exists():
                search_counter =search_event.count()+1
            else:
                search_counter = 1
            data["event_code"]=str(data["name_of_event"])[0:4]
          
            event_seriailizer = EventSerializer(data=data)
            if event_seriailizer.is_valid():
                event_seriailizer.save()
            else:
                return Response(event_seriailizer.errors,status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(event_seriailizer.data,status.HTTP_201_CREATED)
        
        except Exception as E:
            return Response(f'{E}',status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data = request.data
            event = EVENT.objects.get(id=id)
            event_serializer = EventSerializer(event,data=data,partial=True)
            if event_serializer.is_valid():
                event_serializer.save()
            return Response(event_serializer.data,status.HTTP_202_ACCEPTED)
        except Exception as E:
            return Response(f'{E}',status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        try:
            # Fetch the event by id
            event = EVENT.objects.get(id=id)
        except EVENT.DoesNotExist:
            # Handle case where event does not exist
            return Response('Event id does not exist', status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Get the provided password from query parameters
            provided_password = request.query_params.get('password')
            
            # Fetch the event organizer's user model by email
            usermodel = USERMODEL.objects.get(email=event.event_organizer.email)
            
            # Determine the event name
            event_name = event.name_of_event if event.name_of_event else "EVENT TITLE"
            
            # Get the organizer's email
            email_to = usermodel.email
            
            # Check if the provided password matches the organizer's password
            if check_password(provided_password, usermodel.password):
                
                # Delete the event
                if event.event_picture:
                    if os.path.isfile(event.event_picture.path):
                        os.remove(event.event_picture.path)

                event.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response('Incorrect password', status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as E:
            # Handle any unexpected exceptions
            return Response(f'Server error: {E}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
