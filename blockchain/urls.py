from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('add/', views.add_batch, name='add_batch'),
    path('view/', views.view_batch, name='view_batch'),
    path('update/', views.update_batch, name='update_batch'),
    path('check_batch_id/', views.check_batch_id, name='check_batch_id'),
    path('fetch_batch_data/', views.fetch_batch_data, name='fetch_batch_data'),

]
