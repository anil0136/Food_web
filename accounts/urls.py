from django.urls import path
from accounts import views

urlpatterns=[
    path('',views.home,name="home"),
    path('login/',views.user_login,name="login"),
    path('join/',views.auth_choice,name="auth_choice"),
    path('registeration',views.user_registeration,name="registeration"),
    path('home/',views.home,name="home"),
    path('logout/',views.user_logout,name="logout"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('update/',views.update_view,name="update"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
