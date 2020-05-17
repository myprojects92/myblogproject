"""blogfinalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list_view), # for function based pagination
    path('tag/<str:tag_slug>/', views.post_list_view,name='post_list_by_tag_name'),
    #path('', views.PostListView.as_view()),  # for class based pagination
    path('<int:year>/<int:month>/<int:day>/<str:post>/',views.post_detail_view,name='post_detail'),
    path('<int:id>/share/', views.mail_send_view),
]
