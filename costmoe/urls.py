
from django.contrib import admin
from django.urls import path
from costmoeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home1'),
    path('/', views.home, name='home2'),
    path('home/', views.home, name='home3'),
    path('search/', views.ecom, name='search'),
    path('dashboard/', views.admin, name='dashboard'),
    path('scrape_url/', views.scrape_url, name='scrape_url'),
    path('login_c/', views.login_c, name='login_c'),
    path('register/', views.register, name='register'),
    path('login_a/', views.login_a, name='login_a'),
    path('logout/', views.logout_view, name='logout'),
    
]
