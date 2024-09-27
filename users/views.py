from django.shortcuts import render
from users.serializers import *
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.permissions import AllowAny
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render
from decouple import config
from django.http import HttpResponse
from random import randint

def index(request):
    return render(request,'contact_message.html')

@api_view(['PUT'])
@permission_classes([AllowAny])
def change_password(request):
    try:
        data = request.data
        user = USERMODEL.objects.get(email=data['email'])
        password = make_password(data['password'])
        user.password = password
        user.save()

        html_template = 'changed_password.html'
        subject='User Changed their password'
        email_from = config("EMAIL_HOST_USER")
        html_message = render(None, html_template).content.decode()
        message = EmailMessage(subject, html_message,email_from , [user.email])
        message.content_subtype = 'html'
        message.send()
    
        return Response('User Details Updated')
    except Exception as E:
        return Response(f'An Error occurred \n { E }',status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    try:
        email = request.query_params.get('email')
        user = USERMODEL.objects.filter(email=email)

        if user.exists():
            return Response('User exists',status.HTTP_200_OK)
        else:
            return Response('User not found',status.HTTP_404_NOT_FOUND)
    except Exception as E:
        return Response(f'An Error occurred \n { E }',status.HTTP_400_BAD_REQUEST)
    
class send_verification_code(APIView):
    permission_classes = [AllowAny,]
    def get(self,request,email):
        try:
            subject = "Verification Code"
            email_from = config("EMAIL_HOST_USER")
            email_to = email
            verification_code = []
            for i in range(5):
                verification_code.append(str(randint(i,9)))
            
            data = {"verification_code":verification_code}
            html_template = 'verification_code.html'
            html_message = render(None, html_template, data).content.decode()
            message = EmailMessage(subject, html_message, email_from, [email_to])
            message.content_subtype = 'html'
            message.send()

            return Response(verification_code,status.HTTP_200_OK)
        except Exception as E:
            return Response(f'{E}',status.HTTP_400_BAD_REQUEST)
        


class ReceiveFooterMessage(APIView):
    permission_classes=[AllowAny,]
    def post(self,request):
        try:
            data=request.data
            subject = "Welcome to Voteify"
            email_from = config("EMAIL_HOST_USER")
            email_to = data["email"]

            html_template = 'contact_message.html'
            html_message = render(None, html_template, data).content.decode()
            message = EmailMessage(subject, html_message, email_from, [email_to])
            message.content_subtype = 'html'
            message.send()

            html_template = 'contact_message_for_staff.html'
            html_message = render(None,html_template,data).content.decode()
            message = EmailMessage(subject,html_message,email_from,[email_from])
            message.content_subtype='html'
            message.send()


            return Response("Email sent",status.HTTP_200_OK)
        except Exception as E:
            print('\n',E,'\n')
            return Response(f'{E}',status.HTTP_400_BAD_REQUEST)


class Validate_USER(TokenObtainPairView):
    serializer_class = TOKENSERIALIZER
    permission_classes = [AllowAny,]

class REFRESH_USER(TokenObtainPairView):
    serializer_class = REFRESHSERIALIZER

class ShowUsers(APIView):
    permission_classes = [AllowAny,]
    def get(self,request):
        try:
            usermodels = USERMODEL.objects.all()
            user_serializers = USERMODELSERIALIZER(usermodels,many=True)
            return Response(user_serializers.data,status=status.HTTP_200_OK)
        except Exception as E:
            return Response(f'{E} \nan error occurred',status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        try:
            data = request.data
            password = make_password(data['password'])
            usermodel = USERMODEL.objects.create(name=data['name'],password=password,email=data['email'],phone=data['phone'],organization=data['organization'])
            serializer = USERMODELSERIALIZER(usermodel)

            html_template = 'accountregistered.html'
            subject='USER REGISTERED WITH VOTE4YOU'
            email_from = config("EMAIL_HOST_USER")
            html_message = render(None, html_template).content.decode()
            message = EmailMessage(subject, html_message,email_from , [usermodel.email])
            message.content_subtype = 'html'
            message.send()

            return Response(serializer.data,status.HTTP_201_CREATED)
        except Exception as E:
            return Response(f'{E}',status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data =  request.data
            usermodel = USERMODEL.objects.get(id=id)
            user_serializer = USERMODELSERIALIZER(usermodel,data=data,partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            return Response(user_serializer.data,status=status.HTTP_200_OK)
        except Exception as E:
            return Response(f'{E} \nan error occurred',status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            provided_password = request.query_params.get('password')
            usermodel = USERMODEL.objects.get(email=id)
            email_to = usermodel.email
            if check_password(provided_password, usermodel.password):
                usermodel.delete()

                html_template = 'accountdeleted.html'
                subject='User Account Deleted!'
                email_from = config("EMAIL_HOST_USER")
                html_message = render(None, html_template).content.decode()
                message = EmailMessage(subject, html_message,email_from , [email_to])
                message.content_subtype = 'html'
                message.send()
                return Response("User deleted",status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Incorrect password,Unable to delete account",status.HTTP_401_UNAUTHORIZED)
            
        except Exception as E:
            return Response(f'{E} \nan error occurred',status.HTTP_400_BAD_REQUEST)