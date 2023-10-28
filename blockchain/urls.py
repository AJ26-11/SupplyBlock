from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store_data, name='store_data'),
    path('verify/', views.verify_data, name='verify_data'),
    path('view_items/', views.view_items, name='view_items'),
]

