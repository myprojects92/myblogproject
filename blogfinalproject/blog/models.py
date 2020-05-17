from django.db import models
from django.contrib.auth.forms import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    body=models.TextField()
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()
    tags=TaggableManager() # for every post we need to associates tags which will be managed by TaggableManager

    class Meta:
        ordering=['-publish',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%d'),self.publish.strftime('%m'),self.slug])
        # return reverse('post_detail',args=[self.publish.year])
# "?page={{page.next_page_number}}"= it is called 'querystring'
#                                                 -------------

# Models creation for comments section:-->
#-------------------------------------
class Comments(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE) #related_name='comments' it is reverse name which used to get all corresponding comments related to the post
    # here we are not creating 'post' it is already available in the 'Post'. so it is the ForeignKey
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True) # it is required to disable a comment
    class Meta:
        ordering=['-created',]
    def __str__(self):
        return 'commented by {} on {}'.format(self.name,self.post)  #if any person trying to display this comment object by whom and on which post
