
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.views import View
from django.urls import reverse
from .models import CustomUser
from .models import Files
from rest_framework import viewsets
from .serializers import FilesSerializer


@csrf_exempt
def signup(request):
    try:
        if request.method == 'POST':
            data = request.POST
            print(data)
            username = data.get('username')
            print(username)
            email = data.get('email')
            password = data.get('password')

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email is already registered'}, status=400)

            user = CustomUser.objects.create(username=username, email=email, password=password)
            user.save()

            send_verification_email(request, user)

            return JsonResponse({'message': 'Signup successful. Please check your email for verification.'})
        else:
            return JsonResponse({'message': 'inalid request'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        try:
           user= CustomUser.objects.get(username=username , password=password)
           if user.is_active:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
           else:
                return JsonResponse({'error': 'Account not activated. Check your email for verification.'}, status=400)
        except:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    message = f"Hello {user.username},\n\n"
    message += "Please click on the following link to activate your account:\n"
    message += "Thank you."

    user.email_user(subject, message)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Account activated successfully. You can now log in.')
        else:
            return HttpResponse('Activation link is invalid.')
        
        
class FileListView(APIView):
    def get(self, request, *args, **kwargs):
        files = Files.objects.all()
        serializer = FilesSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FilesSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
