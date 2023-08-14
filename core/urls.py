

from django.urls import path

from .views import RegisterView,LoginAPIView,GetProfile,FriendRequestView,GroupListView,GroupChatCreateView,FriendRequestAcceptView

urlpatterns=[
    # path("hello/",hello),
    # path("index/",index),
    # path("chat/<str:username>/", room, name="chat")
    path("register/",RegisterView.as_view(),name='register'),
    path("login/",LoginAPIView.as_view(),name='login'),
    path("userdata/<str:uuid>/",GetProfile.as_view(),name='userdata'),
    path("friendrequest/",FriendRequestView.as_view(),name='friendrequest'),
    path('groupchat/',GroupChatCreateView.as_view(),name='groupchat'),
    path("groupchatlist/",GroupListView.as_view(),name='groupchatlist'),
    path("friendrequestaccept/<str:uuid>/",FriendRequestAcceptView.as_view(),name='friendrequestaccept'),
]