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
)
from account.models import FreelancerProfile, ClientProfile
from account.constants import FREELANCER, CLIENT
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.models import User
from skill_forge.settings import EMAIL_HOST_USER

# Create your views here.


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            account_type = request.session.get("account_type")
            account_category = request.session.get("account_category")
            if account_type == FREELANCER:
                FreelancerProfile.objects.create(
                    user=user,
                    profole_category=account_category,
                    account_type=account_type,
                )
            elif account_type == CLIENT:
                ClientProfile.objects.create(
                    user=user,
                    account_type=account_type,
                )
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            activation_link = reverse("activate", kwargs={"uid64": uid, "token": token})
            activation_url = f"http://{domain}{activation_link}"
            email_subject = "Active Your Account"
            email_body = render_to_string(
                "account/activation_email.html",
                {"user": user, "activation_url": activation_url},
            )

            send_mail(
                email_subject,
                email_body,
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response(
                {
                    "message": "Registration successful. Please check your email to activate your account."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            refresh = RefreshToken(token)
            if refresh.check_blacklist():
                user.is_active = True
                user.save()
                return Response(
                    {"message": "Account activated successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Activation link is invalid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


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

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FreelancerGetProfileView(APIView):
    def get(self, request, *args, **kwargs):
        freelancer_profiles = FreelancerProfile.objects.all()
        serializer = FreelancerGetProfileSerializer(freelancer_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
