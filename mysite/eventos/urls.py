from django.urls import path
from . import views
from django.http import HttpResponseRedirect

urlpatterns = [
    path('', views.home, name='/home'),
    path('list/', views.list_events, name='list_events'),  # sin argumentos
    path('list/<int:event_id>/', views.list_events, name='list_events'),  # sin argumentos
    path('create/', views.create_event, name='create_event'),
    path('delete_event/<str:event_id>/', views.delete_event, name='delete_event'),
    path('edit_event', views.edit_event, name='edit_event'),
    path('register/', views.register_event, name='register_event'),
]
