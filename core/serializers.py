from rest_framework import serializers
from .models import  User,FriendRequest
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # email=serializers.CharField(max_length=68,min_length=6,write_only=True)    

    default_error_messages = {
        'email': 'The email should  be valid'}

    class Meta:
        model = User
        fields = ["username",'first_name',"last_name",'email','mobile','password','profile_photo']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if email.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(
        max_length=68, min_length=6, write_only=True)
    password=serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model=User
        fields=["email","password",'tokens',"uuid"]

    def validate(self,attr):
        email=attr.get("email",None)
        password=attr.get("password",None)
        
        if email is None:
            raise serializers.ValidationError("Email is important")
        if password is None:
            raise serializers.ValidationError("Password is complusory")
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        user=User.objects.get(email=user.email)
        return {
            'email': user.email,
            'tokens': user.tokens,
            'uuid':user.uuid,

        }
                    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["uuid","username","email","first_name","last_name","is_active"]
    
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=FriendRequest
        fields='__all__'
    
    def validate(self,attrs):
        from_friend=attrs.get("from_friend",'')
        to_friend=attrs.get("to_friend",'')
        user=User.objects.get(email=from_friend)
        print(user.friends_list)
        if from_friend == to_friend:
            raise serializers.ValidationError({'recipient': 'You cannot send a friend request to yourself.'})
        if user.friends_list.filter(email=to_friend):
            raise serializers.ValidationError({"error":"User is already in you're friend list"})
        return attrs
    def create(self,validated_data):
        return FriendRequest.objects.create(**validated_data)
    
class AcceptFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model=FriendRequest
        fields="__all__"

