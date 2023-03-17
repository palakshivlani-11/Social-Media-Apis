from .models import *
from rest_framework import serializers

class AddPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Posts
        fields = ['id','title','description','created_at','image']
        

class AddCommentSerializer(serializers.Serializer):
    comment = serializers.CharField()