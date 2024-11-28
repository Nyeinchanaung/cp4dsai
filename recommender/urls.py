from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("result", views.result, name="result"),
    path('detail/<int:result_id>/', views.detail, name="detail"),
]

