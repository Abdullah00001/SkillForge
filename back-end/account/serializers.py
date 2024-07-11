from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import FreelancerProfile, ClientProfile
import requests


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    first_name = serializers.CharField(style={"input_type": "text"}, required=True)
    last_name = serializers.CharField(style={"input_type": "text"}, required=True)
    email = serializers.CharField(style={"input_type": "email"}, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password Do Not Match")
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    "username": user.username,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")


class UserAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]


class FreelancerProfieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerProfile
        exclude = ("user",)


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        exclude = ("user",)


class FreelancerProfileUpdateSerializer(serializers.Serializer):
    user = UserAccountUpdateSerializer()
    profile = FreelancerProfieSerializer()
    profile_image = serializers.ImageField(write_only=True, required=False)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        profile_data = validated_data.pop("profile")
        profile_image = validated_data.pop("profile_image", None)

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        if profile_image:
            image_url = self.upload_image_to_imagebb(profile_image)
            profile_data["profile_image"] = image_url

        for attr, value in profile_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def upload_image_to_imagebb(self, image):
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "b85dfbc11f4220b41411436977a60d47",
            "image": image.read(),
        }
        response = requests.post(url, payload)
        response_data = response.json()
        return response_data["data"]["url"]


class ClientProfileUpdateSerializer(serializers.Serializer):
    user = UserAccountUpdateSerializer()
    profile = ClientProfileSerializer()
    profile_image = serializers.ImageField(write_only=True, required=False)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        profile_data = validated_data.pop("profile")
        profile_image = validated_data.pop("profile_image", None)

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        if profile_image:
            image_url = self.upload_image_to_imagebb(profile_image)
            profile_data["profile_image"] = image_url

        for attr, value in profile_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def upload_image_to_imagebb(self, image):
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "b85dfbc11f4220b41411436977a60d47",
            "image": image.read(),
        }
        response = requests.post(url, payload)
        response_data = response.json()
        return response_data["data"]["url"]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("The new passwords do not match.")
        validate_password(data["new_password"], self.context["request"].user)
        return data

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class FreelancerGetProfileSerializer(serializers.ModelSerializer):
    user = UserGetSerializer()

    class Meta:
        model = FreelancerProfile
        fields = "__all__"
