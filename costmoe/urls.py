
from django.contrib import admin
from django.urls import path
from costmoeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home1'),
    path('/', views.home, name='home2'),
    path('home/', views.home, name='home3'),
    path('search/', views.ecom, name='search'),
]
