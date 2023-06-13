from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tc/', views.get_tc, name='tc'),
    path('rev/', views.get_rev, name='tc'),
    path('pp/', views.get_privacy_policy, name='pp'),
]