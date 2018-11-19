from django.urls import path, include
from . import views

#to handle my app urls
app_name = 'emanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('logout', views.log_out, name='logout'),
    path('add', views.add_expense, name='add_expense'),
]