from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('ex1/', views.Example1View.as_view(), name='ex1'),
    path('ex2/', views.Example2View.as_view(), name='ex2'),
]
