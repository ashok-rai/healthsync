"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path, include
# from accounts import views as user_views
# from django.contrib.auth import views as auth_views  # Authentication views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('register/', user_views.register, name='register'),
#     path('login/', user_views.UserLoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('', user_views.dashboard, name='home'),
# ]

from django.contrib import admin
from django.urls import path, include
from .views import dashboard
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('accounts/', include('allauth.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('appointments/', include('appointments.urls')),
    path('payments/', include('payments.urls')),
    path('notifications/', include('notifications.urls')),
]