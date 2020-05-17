from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from blog.forms import EmailSendForm,CommentsForm
from taggit.models import Tag
# Create your views here.

# TO DO PAGINATION BY classbased view():--->>
#---------------------------------------
from django.views.generic import ListView

#class PostListView(ListView):
#    model=Post
#    paginate_by=2
    # default template=page_list.html
    # default object in post_list.html = page_obj
                               #       ----------

# TO DO PAGINATION BY  FUNCTION BASED VIEW():-->
#--------------------------------------------

def post_list_view(request,tag_slug=None):  #tag_slug=None is the keyward argument and the default value is None i.e if I am not passing anything the default value is None and only post_list value will be shown to us
    post_list=Post.objects.all()
    tag=None
    if tag_slug:    # if we are passing tag_slug i.e clicking a tag
        tag=get_object_or_404(Tag,slug=tag_slug)   #can u plz provide the tag object where slug is our provided slug related to tag_slug(i.e provided tag value) value from Tag model
        post_list=post_list.filter(tags__in=[tag]) #post related to this particular filter 'tags__in=[tag]' we are filtering. and it will dispaly posts related to the particular filtered post only based on tag_slug
    paginator=Paginator(post_list,2)    # THIS IS FOR FUNCTION BASED PAGINATION
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})

## Here tags__in=[tag] means tags related to this particular post is the specified tag can u plz get that tag related posts only

#--------------------------------------------------------------------------------
def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published')
    comments=post.comments.filter(active=True) # display all comments related to this post where active=True only
    csubmit=False #csubmit means commentsubmit
    if request.method=='POST':
        form=CommentsForm(request.POST) # it contains CommentsForm form data
        if form.is_valid():
            new_comment=form.save(commit=False) #commit=False  means don't save the comments in the database now
            new_comment.post=post  # related to the current post assign the comment for post field i.e new_comment.post
            new_comment.save()
            csubmit=True    #csubmit means commentsubmit
    else:
        form=CommentsForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})  #TO DISPLAY POST WITHOUT NO. OF VISITORS TO WEBSITE
#    count=int(request.COOKIES.get('count',0)) #IT MEANS HEY COOKIE DO YOU HAVE ANY COOKIE NAMED WITH COUNT IF NOT THEN RETURN COOKIE IS 0
#    newcount=count+1                                                                                       #IF YES THEN PROVIDE THE COOKIE VALUE
#    response=render(request,'blog/post_detail.html',{'post':post,'count':newcount})
#    response.set_cookie('count',newcount,max_age=180) #TO SET COOKIES FOR 3 MINUTES I.E 180 SECONDS WE HAVE TO WRITE IN THIS MANNER AND IT IS CALLED PERSISTENT COOKIES
#    return response


# share by email code vvv imp:-----
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')  #i.e from Post Model can u create post object, based on the id(def mail_send_view(request,id) can u plz provide me the published post_list
    sent=False  # for GET request sent value is False
    if request.method=='POST':
        form=EmailSendForm(request.POST) # it contains form data
        if form.is_valid():
            cd=form.cleaned_data  # form.cleaned_data  means enduser provided data and it is in the form of dictionary
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)  #it is called string formatting where {}=name,{}=email,{}=post ttile
            post_url=request.build_absolute_uri(post.get_absolute_url()) # it is used to get full url
            message='Read the post at:\n{}\n\n{}\'s comments:\n{}'.format(post_url,cd['name'],cd['comments']) # to use single quote as a symbol we have to use \''
            send_mail(subject,message,'hello@blog.com',[cd['to']]) # its way to send mail i.e share a post to any email
            # its format is send_mail(subject,message,'sender email id','receiver') and [cd['to']] means it is expecting a list
            sent=True   # for POST request sent value is Fale
    else:
        form=EmailSendForm()  #creation of form object
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent}) # whem mail_send_view is called it will display the form i.e EmailSendForm
# in html target="_blank" means it will open a new tab/page in browser
# for GET request sent value is False
# to use single quote as a symbol we have to use \''
#TO GET COMPLETE URL WHILE MAIL SENDING:-> 'build_absolute_uri' will generate http://127.0.0.1:8000  AND 'get_absolute_url()'' will generate 2019/05/10/django-information/  so the total url will be http://127.0.0.1:8000/2019/05/10/django-information/
