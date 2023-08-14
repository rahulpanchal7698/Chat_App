

from django.urls import path

from .views import RegisterView,LoginAPIView,GetProfile,FriendRequestView,FriendRequestAcceptView

urlpatterns=[
    # path("hello/",hello),
    # path("index/",index),
    # path("chat/<str:username>/", room, name="chat")
    path("register/",RegisterView.as_view(),name='register'),
    path("login/",LoginAPIView.as_view(),name='login'),
    path("userdata/<str:uuid>/",GetProfile.as_view(),name='userdata'),
    path("friendrequest/",FriendRequestView.as_view(),name='friendrequest'),
    path("friendrequestaccept/<str:uuid>/",FriendRequestAcceptView.as_view(),name='friendrequestaccept'),
]