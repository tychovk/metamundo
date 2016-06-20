"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from app import views


urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^world/new$', views.new_world, name='new_world'),
    url(r'^world/(\d+)/$', views.view_world, name='view_world'),
    url(r'^world/(\d+)/add_blob$', views.add_blob, name='add_blob'),
    url(r'^grid/(\d+)/$', views.view_grid, name='view_grid'),
    url(r'^grid/new$', views.new_grid, name='new_grid'),
    #url(r'^admin/', admin.site.urls),
    
]
