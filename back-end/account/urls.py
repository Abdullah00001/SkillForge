from django.urls import path
from account.views import (
    UserRegistrationView,
    ActivateAccountView,
    LoginView,
    ClientProfileUpdateView,
    FreelancerProfileUpdateView,
    PasswordChangeView,
    LogoutView,
    FreelancerGetProfileView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "profile/freelancer/update/",
        FreelancerProfileUpdateView.as_view(),
        name="freelancer-profile-update",
    ),
    path(
        "profile/client/update/",
        ClientProfileUpdateView.as_view(),
        name="client-profile-update",
    ),
    path(
        "profile/password-change/", PasswordChangeView.as_view(), name="password-change"
    ),
    path("profile/logout/", LogoutView.as_view(), name="logout"),
    path(
        "get-freelancer-profiles/",
        FreelancerGetProfileView.as_view(),
        name="get-freelancer-profiles",
    ),
]
