from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    # APIs
    path('api/register/', views.register_api, name='api-register'),
    path('api/login/', views.login_api, name='api-login'),
    path('api/profile/', views.profile_api, name='api-profile'),
]