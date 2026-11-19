from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('learn/<slug:slug>/', views.pillar_detail, name='pillar_detail'),
    path('learn/<slug:pillar_slug>/<slug:chapter_slug>/',
         views.chapter_detail, name='chapter_detail'),
    path('learn/<slug:pillar_slug>/<slug:chapter_slug>/quiz/',
         views.take_quiz, name='take_quiz'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('certificate/<uuid:certificate_id>/',
         views.certificate_view, name='certificate_view'),

    path('forum/', views.forum, name='forum'),
    path('forum/new/', views.forum_new, name='forum_new'),
    path('forum/<int:pk>/', views.forum_topic, name='forum_topic'),

    path('live/', views.live_sessions, name='live_sessions'),

    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(
         template_name='auth/signin.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/',
     auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),
     name='password_reset'),
path('accounts/password_reset/done/',
     auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
     name='password_reset_done'),
path('accounts/reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
     name='password_reset_confirm'),]

