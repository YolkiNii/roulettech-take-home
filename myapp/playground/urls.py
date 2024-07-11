from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("csrf/", views.csrf, name="csrf"),
    path("<int:blog_id>/", views.comments, name="comments"),
]