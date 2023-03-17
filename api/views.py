from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import *
from rest_framework import generics, permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .serializers import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def follow(request):
    if request.method == 'POST':
        id = request.query_params.get('id')
        curr = request.user
        try:
            followid = User.objects.get(id=id)
            soc = socialmediaprofile.objects.get(user=curr)
            target = socialmediaprofile.objects.get(user=followid)
        except ObjectDoesNotExist:
            return Response({'Error':'User not found'},status=406)
        data = {}
        try:
            check = soc.following.get(user=followid)
            data['response'] = 'Already Following this user'
        except:
            target.follower.add(soc)
            soc.following.add(target)
            data['response'] = curr.username + " started following " + followid.username
        return Response(data,status=200)
            
@api_view(['POST'])
@permission_classes((IsAuthenticated,)) 
@csrf_exempt
def unfollow(request):
    if request.method == 'POST':
        id = request.query_params.get('id')
        curr = request.user
        try:
            unfollowid = User.objects.get(id=id)
            source = socialmediaprofile.objects.get(user=curr)
            target = socialmediaprofile.objects.get(user=unfollowid)
        except ObjectDoesNotExist:
            return Response({'Error':'User not found'},status=406)
        data = {}
        try:
            check = source.following.get(user=unfollowid)
            source.following.remove(target)
            target.follower.remove(source)
            data['response'] = curr.username + "unfollowed" + unfollow.username
        except:
            data['response'] = 'Already Unfollowed this user'
            return Response(data,status=200)
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getuserprofile(request):
    if request.method == 'GET':
        curr = request.user
        try:
            sop = socialmediaprofile.objects.get(user=curr)
        except ObjectDoesNotExist:
            return Response({'Error':'User Social Profile not found'},status=406)
        data = {}
        data['name'] = curr.username
        data['followers'] = sop.follower.all().count()
        data['following'] = sop.following.all().count()
        return Response(data,status=200)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def addposts(request):
    if request.method == 'POST':
        curr = request.user
        serializer = AddPostSerializer(data=request.data)
        if serializer.is_valid():
            obj = Posts.objects.create(user=curr,title=serializer.validated_data['title'],description=serializer.validated_data['description'],image=serializer.validated_data['image'])
            data = {}
            data['id'] = obj.id
            data['created_at'] = obj.created_at
            data['title'] = obj.title
            data['description'] = obj.description
            return Response(data,status=200)
        else:
            return Response(serializer.errors,status=406)
        
@api_view(['DELETE','GET'])
@permission_classes((IsAuthenticated,))
def deletepost(request):
    if request.method == 'DELETE':
        id = request.query_params.get('id')
        curr = request.user
        try:
            dpost = Posts.objects.get(id=id)
            if dpost.user == curr:
                dpost.delete()
                return Response({'Response':'Post Deleted'},status=200)
            else:
                return Response({'Response':'Not Your Post'},status=500)
        except ObjectDoesNotExist:
            return Response({'Error':'Post ID not found'},status=406)
    elif request.method == 'GET':
        id = request.query_params.get('id')
        try:
            post = Posts.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'Error':'Post ID not found'},status=406)
        data = {}
        data['number-likes'] = Likes.objects.filter(post=post,like=True).count()
        data['number-comments'] = Comments.objects.filter(post=post).count()
        data['title'] = post.title
        data['desc'] = post.description
        return Response(data,status=200)
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def likepost(request):
    if request.method == 'POST':
        id = request.query_params.get('id')
        curr = request.user
        try:
            lpost = Posts.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'Error':'Post ID not found'},status=406)
        try:
            check = Likes.objects.get(user=curr,post=lpost)
            if check.like == True:
                return Response({'Response':'Already Liked'},status=200)
            else:
                check.like = True
                check.save()
                return Response({'Response':'Post Liked'},status=200)
        except:
            Likes.objects.create(user=curr,like=True,post=lpost)
            return Response({'Response':'Post Liked'},status=200)
        
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def unlikepost(request):
    if request.method == 'POST':
        id = request.query_params.get('id')
        curr = request.user
        try:
            ulpost = Posts.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'Error':'Post ID not found'},status=406)
        try:
            check = Likes.objects.get(user=curr,post=ulpost)
            check.delete()
            return Response({'Response':'unliked'},status=200)
        except:
            return Response({'Response':'Post Already Unliked'},status=200)
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def AddComment(request):
    if request.method == 'POST':
        id = request.query_params.get('id')
        curr = request.user
        serializer = AddCommentSerializer(data=request.data)
        try:
            cpost = Posts.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'Error':'Post ID not found'},status=406)
        if serializer.is_valid():
            obj = Comments.objects.create(user=curr,post=cpost,comment=serializer.validated_data['comment'])
            data={}
            data["Comment-Id"] = obj.id
            return Response(data,status=200)
        else:
            return Response(serializer.errors,status=406)
        
        
        
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getallposts(request):
    if request.method == 'GET':
        curr = request.user
        objs = Posts.objects.filter(user=curr).order_by('-created_at')
        data = []
        for obj in objs:
            dat = {}
            dat['id'] = obj.id
            dat['title'] = obj.title
            dat['desc'] = obj.description
            dat['created_at'] = obj.created_at
            com = Comments.objects.filter(post=obj)
            dat['comments'] = []
            for comu in com:
                du = {}
                du['comment'] = comu.comment
                du['user'] = comu.user.username
                du['time'] = comu.commented_time
                dat['comments'].append(du)
            dat['number-likes'] = Likes.objects.filter(post=obj,like=True).count()
            data.append(dat)
        return Response(data,status=200)

            
