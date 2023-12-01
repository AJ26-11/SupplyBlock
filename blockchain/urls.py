from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store_data, name='store_data'),
    path('verify/', views.verify_data, name='verify_data'),
    path('view_items/', views.view_items, name='view_items'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('add_batch/', views.add_batch, name='add_batch'),
    path('process_batch/', views.process_batch, name='process_batch'),
    path('package_batch/', views.package_batch, name='package_batch'),
    path('ship_batch/', views.ship_batch, name='ship_batch'),
    path('deliver_batch/', views.deliver_batch, name='deliver_batch'),
    path('view_batch_details/', views.view_batch_details, name='view_batch_details'),

]
