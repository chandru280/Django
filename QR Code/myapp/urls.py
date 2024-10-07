from django.urls import path 
from myapp import views
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [


    path('', views.add_qrcode, name='add_qrcode'),
    path('qrcode/<int:qrcode_id>/', views.qrcode_detail, name='qrcode_detail'),
    path('sample/<int:pk>/', views.sample_detail, name='sample_detail'),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

