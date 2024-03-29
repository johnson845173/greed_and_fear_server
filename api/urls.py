from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log/', views.log_user_view, name='log'),
    path('sample/<str:file_name>/', views.sample_pdf, name='log'),
    path('simple/<str:file_name>/', views.simple_pdf, name='log'),
    path('viewpdf/<str:file_name>/', views.view_pdf, name='log'),
    path('razorpay/webhook/', views.razorpay_update, name='razorpay'),

    path('tc/', views.get_tc, name='tc'),
    path('rev/', views.get_rev, name='tc'),
    path('pp/', views.get_privacy_policy, name='pp'),
    path('login/', views.login, name='login_api'),
    path('preorder/', views.preorder, name='preorder'),

    path('bans/update/', views.update_sebi_bans_view, name='preorder'),
    path('bans/get/', views.get_sebi_bans_view, name='preorder'),

    path('user/remind/', views.send_reminder, name='send_reminder'),

    path('otp/send/', views.send_whatspp_otp_view, name='send_reminder'),
    path('otp/validate/', views.validate_whatspp_otp_view, name='send_reminder'),

    path('stocks/intra/', views.get_intra_stock, name='login_api'),
    path('stocks/indices/', views.get_indices_stock, name='login_api'),

    path('db/clear/', views.clear_db, name='login_api'),
]