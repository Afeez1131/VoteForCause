from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name='home'),
    path("", views.home, name="home"),
    path("tag/<tag_slug>/", views.tag_view, name="tag_view"),
    path("cause/create/", views.create_cause, name="create_cause"),
    path("cause/<slug>/", views.cause_detail, name="cause_detail"),
    path("cause/signed/<slug>/", views.cause_signed_userlist, name="cause_sign_list"),
    path("cause/update/<slug>/", views.cause_update, name="update_cause"),
    path("cause/delete/<slug>/", views.cause_delete, name="delete_cause"),
    path("cause/sign/add/<slug>/", views.add_sign_cause, name='add_sign'),
]
