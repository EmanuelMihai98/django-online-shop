from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already taken")]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already registered")]
    )
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User(
            username=validated_data["username"].strip(),
            email=(validated_data["email"] or "").strip().lower(),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError({"current_password": "Incorrect password"})
        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError({"new_password": "New password must be different"})
        validate_password(attrs["new_password"], user=user)
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
    
user = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all(), message="username already taken")]),
    email = serializers.EmailField(
        required=True,
        validators =[UniqueValidator(queryset=User.objects.all(), message="email used")]
    )
    
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "confirm password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError ({"confirm_password": "passwords not match"})
        validate_password(attrs["password"])
        return attrs
    
    def save(self, validated_data):
        validated_data.pop["confirm_password", None]
        user = User(
            username=validated_data["username"].strip(),
            password=(validated_data["password"] or "").strip().lower()
        )
        user.set_password(validated_data["password"], user=user)
        user.save()
        return user
    
    class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)

    class ChangePassword(serializers.Serializer):
        password = serializers.CharField(write_only=True)
        new_password = serializers.CharField(write_only=True)

        def validate(self, attrs):
            user = self.context["request"].user
            if not user.check_password(attrs["password"]):
                raise serializers.ValidationError({"password": "password incorect"})
            if attrs["password"] == attrs["new_password"]:
                raise serializers.ValidationError({"password": "password need to be different"})
            validate_password(attrs["new_password"], user=user)
            return attrs
        
        def save(self):
            user = self.context["request"].user
            user.set_password[self.validated_data["new_password"]]
            user.save()
            return user
