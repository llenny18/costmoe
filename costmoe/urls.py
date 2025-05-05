
from django.contrib import admin
from django.urls import path
from costmoeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home1'),
    path('/', views.home, name='home2'),
    path('home/', views.home, name='home3'),
    path('search/', views.ecom, name='search'),
    path('monitored_products/', views.ecom_choosen, name='monitored_products'),
    path('analyze/', views.best_products_view, name='analyze'),
    path('dashboard/', views.admin, name='dashboard'),
    path('products/', views.products, name='products'),
    path('admins/', views.admins, name='admins'),
    path('customers/', views.customers, name='customers'),
    path('scrape_url/', views.scrape_url, name='scrape_url'),
    path('login_c/', views.login_c, name='login_c'),
    path('register/', views.register, name='register'),
    path('login_a/', views.login_a, name='login_a'),
    path('logout/', views.logout_view, name='logout'),
    path('everif/', views.everif, name='everif'),
    path('quotations/', views.quotations, name='quotations'),
    path('analyze_csv/<int:c_id>/', views.analyze_csv, name='analyze_csv'),
    path('market_differentiation/', views.market_differentiation_view, name='market_differentiation'),
    path('api/products/', views.products_api, name='products_api'),
    path('api/fetch-products/', views.fetch_products, name='fetch_products'),
    
    
]
