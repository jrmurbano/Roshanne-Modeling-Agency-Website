from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('models/', views.models, name='models'),
    path('contact/', views.contact, name='contact'),
    path('photoshoots/', views.photoshoots, name='photoshoots'),
    path('magazines/', views.magazines, name='magazines'),
    path('runways/', views.runways, name='runways'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('shopping-bag/', views.shopping_bag, name='shopping_bag'),
    path('add-to-bag/<int:item_id>/', views.add_to_bag, name='add_to_bag'),
    path('update-bag/<int:item_id>/', views.update_bag, name='update_bag'),
    path('remove-from-bag/<int:item_id>/', views.remove_from_bag, name='remove_from_bag'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
]