from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('mygames', views.mygames, name='mygames'),
    path('merchants', views.merchants, name='merchants'),
    path('product/<int:product_id>', views.product, name='product'),
    path('product/<int:product_id>/buy', views.product_buy, name='product_buy'),
    path('product/add', views.product_add, name='add_product')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)