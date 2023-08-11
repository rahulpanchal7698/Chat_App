from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import Message,ChatRoom,User
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework import generics ,response,status,views,serializers
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens  import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        user=User.objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user).access_token
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'https://'+current_site+relativeLink+"?token="+str(token)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class GetProfile(views.APIView):
    serializer_class=UserSerializer
    permission_classes=(IsAuthenticated,)
    def get_object(self, uuid):
        try:
            return User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            raise serializers.ValidationError("No User")
    def get(self, request, uuid, format=None):
        snippet = self.get_object(uuid)
        serializer = UserSerializer(snippet)
        return response.Response(serializer.data)
# User=get_user_model()

# def hello(request):
#     return HttpResponse("Hello")

# def index(request):
#     users=User.objects.exclude(username=request.user.username)
#     return render(request, "chats/index.html",{"users":users})

# def room(request, username):
#     user_obj=User.objects.get(username=username)
#     user_objs=User.objects.get(username=username).id
#     users=User.objects.exclude(username=request.user.username)
#     if request.user.id >user_objs:
#         thread_name = f'chat_{request.user.id}-{user_obj.id}'
#     else:
#         thread_name = f'chat_{user_obj.id}-{request.user.id}'
#     room = ChatRoom.objects.get(name=thread_name)
#     messages_objs=Message.objects.filter(room=room)
#     return render(request, "chats/room.html", {"user": user_obj.username,"users":users,"user_id":user_objs,"messages_obj":messages_objs})
