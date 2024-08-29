from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    FreelancerProfileUpdateSerializer,
    ClientProfileUpdateSerializer,
    PasswordChangeSerializer,
    FreelancerGetProfileSerializer,
    ClientGetProfileSerializer,
)
from account.models import FreelancerProfile, ClientProfile
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from skill_forge.settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_url = f"http://127.0.0.1:8000/account/activate/{uid}/{token}/"
            email_subject = "Activate Your Account"
            email_body = render_to_string(
                "account/activation_email.html",
                {"user": user, "activation_url": activation_url},
            )

            try:
                send_mail(
                    email_subject,
                    "",
                    EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                    html_message=email_body,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to send activation email."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {
                    "message": "Registration successful. Please check your email to activate your account."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            
            return HttpResponseRedirect(
                "http://127.0.0.1:5500/front-end/pages/main.html"
            )
        else:
            return HttpResponseRedirect(
                "http://127.0.0.1:5500/front-end/pages/activation_error.html"
            )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, "user_id": user.id})

            else:
                return Response({"error": "Invalid Credential"})
        return Response(serializer.errors)


class FreelancerProfileUpdateView(APIView):

    def put(self, request):
        user_profile = request.user.freelancer_account
        serializer = FreelancerProfileUpdateSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientProfileUpdateView(APIView):

    def put(self, request):
        user_profile = request.user.client_account
        serializer = ClientProfileUpdateSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):

    def put(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class FreelancerGetProfileView(APIView):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user_name"]

    def get(self, request, *args, **kwargs):
        user_name = request.query_params.get("user_name", None)
        freelancer_profiles = FreelancerProfile.objects.all()
        serializer = FreelancerGetProfileSerializer(freelancer_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientGetProfileView(APIView):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user_name"]  # Change to user_name

    def get(self, request, *args, **kwargs):
        user_name = request.query_params.get("user_name", None)  # Change to user_name
        freelancer_profiles = ClientProfile.objects.all()

        # Filter profiles if a user_name is provided
        if user_name:
            freelancer_profiles = freelancer_profiles.filter(
                user__username__icontains=user_name
            )

        serializer = ClientGetProfileSerializer(freelancer_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
