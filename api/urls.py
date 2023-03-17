from .views import *
from django.urls import path , include


urlpatterns = [
    path('follow/', follow, name="follow"),
    path('unfollow/', unfollow, name="unfollow"),
    path('user', getuserprofile, name="user"),
    path('posts', addposts, name="posts"),
    path('posts/', deletepost, name="posts"),
    path('like/', likepost, name="like"),
    path('unlike/', unlikepost, name="unlike"),
    path('comment/', AddComment, name="comment"),
    path('all_posts', getallposts, name="all_posts"),
]

