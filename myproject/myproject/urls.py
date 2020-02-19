"""myproject URL Configuration

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

from boards import views
from accounts import views as accounts_views

# TODO: format URLs to individual apps instead of main project URL
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', accounts_views.signup, name='signup'),
    path('boards/', views.board_redirect),
    path('boards/<int:board_id>/', views.board_topics, name='board_topics'),
    path('boards/<int:board_id>/new/', views.new_topic, name='new_topic'),
]

'''
Changed URL to PATH
boards: url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics)
argument must match what's inside <...> in the tutorial, argument in function becomes 
def board_topics(request, pk): ...
Sice we did <int:board_id>, argument in function becomes
def board_topics(request, board_id): ...
A 
'''
