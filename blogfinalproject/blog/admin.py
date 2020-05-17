from django.contrib import admin
from blog.models import Post,Comments

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','body','author','publish','created','updated','status']
    list_filter=['status','author','created','publish']
    search_fields=('title','body')
    raw_id_fields=('author',) # comma is needed because its a  tuple
    date_hierarchy='publish'
    ordering = ['status','publish']
    prepopulated_fields = {'slug': ('title',)}

class CommentsAdmin(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated','active']
    list_filter=['created','updated','active']
    search_fields=('name','email','body')


admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentsAdmin)
