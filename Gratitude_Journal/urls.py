"""Gratitude_Journal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from journals import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<user_slug>', views.profile, name='profile'),
    path('journal/<journal_slug>', views.journal_detail, name='journal_detail'),
    path('explore/', views.explore, name='explore'),
    path('follow/', views.follow_user, name='follow_user'),
    path('feed/', views.feed, name='feed'),
    path('delete_journal/', views.delete_journal, name='delete_journal'),
    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form_custom.html'),
         name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/password_change/done',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done_custom.html'),
         name='password_change_done'),
    path('accounts/password_reset',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form_custom.html'),
         name='password_reset'),
    path('accounts/password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_custom.html'),
         name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm_custom.html'),
         name='password_reset_confirm'),
    path('accounts/password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_custom.html'),
         name='password_reset_complete'),
    path('accounts/register', views.register, name='register'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
