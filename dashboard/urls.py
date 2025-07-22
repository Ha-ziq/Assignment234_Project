from django.urls import path
from dashboard.views import dashboard, classic_preview, modern_preview, creative_preview, technical_preview

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('classic/', classic_preview, name='classic_preview'),
    path('modern/', modern_preview, name='modern_preview'),
    path('creative/', creative_preview, name='creative_preview'),
    path('technical/', technical_preview, name='technical_preview'),
]