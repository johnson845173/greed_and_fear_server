from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log/', views.log_user_view, name='log'),
    path('razorpay/webhook/', views.razorpay_update, name='razorpay'),
    path('tc/', views.get_tc, name='tc'),
    path('rev/', views.get_rev, name='tc'),
    path('pp/', views.get_privacy_policy, name='pp'),
    path('login/', views.login, name='login_api'),
    path('stocks/intra/', views.get_intra_stock, name='login_api'),
]