from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include("MultipeChoiceTest.urls")),

    path('accounts/login/', auth_views.LoginView.as_view),
    path('accounts/logout/', auth_views.LogoutView.as_view),
]
