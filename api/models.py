from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class socialmediaprofile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='socialmediaprofile')
    follower = models.ManyToManyField('self', blank=True, related_name="user_followers",symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name="user_following",symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s' % (self.user)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        socialmediaprofile.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.socialmediaprofile.save()
        
class Posts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    
    class Meta:
        ordering = ['-pk']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Posts, self).save(*args, **kwargs)
        

class Comments(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    commented_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.email + self.comm)
    
class Likes(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.user.email + str(self.like))