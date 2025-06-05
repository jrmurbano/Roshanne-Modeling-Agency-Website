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
]