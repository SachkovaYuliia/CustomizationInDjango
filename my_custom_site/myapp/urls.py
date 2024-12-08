from django.urls import path
from . import views
from .views import CustomModelListView, register, request_count_view

urlpatterns = [
    path('', views.custom_form_view, name='custom_select'),
    path('success/', views.success_view, name='success_view'),
    path('processor/', views.processor_view, name='context_processor'),
    path('custom-models/', CustomModelListView.as_view(), name='custom_model_list'),
    path('register/', register, name='register'),
path('metrics/', request_count_view, name='metrics'),
]
