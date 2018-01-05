from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('signup/', views.signup, name = "user_signup"),
    path('login/', views.login_user, name = "user_login"),
    path('logout/', views.logout_user, name = "user_logout"),
    re_path(r'^home/(?P<username>\w+([.| ]\w+)*)/', views.homepage, name = "user_home"),#note the regex ; this is to match usernames ending in sucessions of . followed by initial
    re_path(r'', views.app_home, name = 'application_home'),
]
