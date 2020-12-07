from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register', views.registration_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('login', views.login_view, name="login"),
    path('account', views.account_view, name="account"),
    path('profile', views.profile_view, name="profile"),


    path('users_list', views.user_list, name="user_list"),
    path('user_profile/<username>', views.user_profile, name="user_profile"),
    path('topcontributors', views.topContributors, name="topContributors"),


    path('must_authenticate', views.must_authenticate_view,
         name="must_authenticate"),

    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),

]
