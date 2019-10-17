from django.urls import path, re_path
from . import views

app_name = 'registration'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    re_path('payment-success/(?P<rg_id>\d+)/$',
            views.PaymentSucessView.as_view(),
            name='payment-success'),
    re_path('^payment-cancel/(?P<rg_id>\d+)/(?P<tnx_id>[a-z0-9]{32})/$',
            views.CancelResponseView.as_view(),
            name='payment-cancel'),
    path('thank-you/', views.ThankYouView.as_view(), name='thank-you'),
    path('error/', views.NoScriptView.as_view(), name='no-script')
]
