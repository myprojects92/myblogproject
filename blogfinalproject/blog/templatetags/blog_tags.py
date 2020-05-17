# CREATION OF OUR OWN TEMPLATETAGS I.E CUSTOM TEMPLATE TAGS:----(THERE ARE TOTAL 3 TAGS: 1)SIMPLE_TAG 2)INCLUSION_TAG..THERE IS  NO ASSIGNMENT_TAG IN DJANGO 2.0 OMWARDS
#===========================================================
#Step-1:-- first create a folder inside application folder(here it is blog) named as 'templatetags'(it is predefined we can't change its name)
#Step-2:-- then inside templatetags folder create 2 files such as '__init__.py'(predefined and it is mandatory) and 'blog_tags.py'(any name we can give)

from blog.models import Post
from django import template  #when the following function acts as template tag(i.e our own template tag) We have to register with the template library
register=template.Library()  #when the following function acts as template tag(i.e our own template tag) We have to register with the template library

#USAGE OF SIMPLE_TAG TO RETURN NO. OF POSTS PUBLISHED:---(SIMPLE_TAG:-- IT PERFORM SOME PROCESSING AND RETURNS A STRING)
#====================================================

@register.simple_tag#(name='my_tag')   #register of this function as template tag in this manner
def total_posts():
    return Post.objects.count()  # here it will act as 'template'
# IF WE ARE TAKING name='my_tag' THEN WE HAVE TO SPECIFY IN BASE.HTML FILE INSTEAD OF {%total_posts%} AS:--> <p>Total number posts published till today:<span id="pcount">{%my_tag%}</span> </p>

#USAGE OF INCLUSION_TAG TO DISPLAY LATEST POSTS:---(INCLUSION_TAG:-- IT PERFORM SOME PROCESSING AND RETURNS A RENDERED TEMPLATE)
#====================================================

@register.inclusion_tag('blog/latest_posts123.html')  # blog/latest_posts123.html:---> it means inclusion of this template because inclusion_tag returns a rendered template
def show_latest_posts(count=3):  #(count=3 means by default it will display 3 posts in Latest posts if any count value not specified in sidebar of base.html)
    latest_posts=Post.objects.order_by('-publish')[:count]#[:3] (here instead of hard coding([:3]) we are passing count value which we will get in base.html template tag:--> {%show_latest_posts 4%}
    return {'latest_posts':latest_posts}

#USAGE OF SIMPLE_TAG TO DISPLAY THE MOST COMMENTED POSTS:---(ASSIGNMENT_TAG:-- IT PERFORM SOME PROCESSING AND ASSIGN THE RESULT TO THE VARIABLE IN THE CONTEXT)
#====================================================
from django.db.models import Count
@register.simple_tag
def get_most_commented_posts(count=4):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
# annotate(total_comments=Count('comments')):--->job of annotate:- it means can u plz 'count the comment' and then assign it to 'total_comments'. it is the job of 'annoatate'
