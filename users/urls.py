from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="account_login"),
    path("logout/", views.CustomLogoutView.as_view(), name="account_logout"),
    path("profile/", views.ProfileView, name="profile"),
    path("signup/", views.CustomSignupView.as_view(), name="account_signup"),
    # path('password/change/', views.CustomPasswordChangeView.as_view(),
    # name='account_change_password'),
]
