from django.contrib import admin
from .models import User,FriendRequest,GroupChatRoom
# Register your models here.


admin.site.register(User)
admin.site.register(FriendRequest)
admin.site.register(GroupChatRoom)
# admin.site.register(ChatRoom)
# admin.site.register(Message)
