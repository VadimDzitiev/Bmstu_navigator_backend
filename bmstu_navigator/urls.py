from django.contrib import admin
from django.urls import path
from bmstu import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetCampuses),
    path('transition/<int:id>/', views.GetCampus, name='campus_url'),
]


