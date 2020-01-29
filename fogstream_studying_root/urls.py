from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_view, name='page_view'),
    path('qr_code', views.qr_gen, name='qr_gen'),
    path('qr_read_view', views.qr_read_view, name='qr_read_view'),
    path('reg_on_lecture', views.reg_on_lecture, name='reg_on_lecture'),
]