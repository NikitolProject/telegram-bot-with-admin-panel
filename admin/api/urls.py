from django.urls import path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import (
    user as user_views,
    swear_word as swear_word_views,
)
from rest_framework.routers import DefaultRouter
                                        

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='swagger-ui', permanent=False)),

    # Swagger and schema
    path('doc', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema', SpectacularAPIView.as_view(), name='schema'),

    path('telegram-user', user_views.CreateTelegramUser.as_view(), name='telegram-user'),
    path('swear-word', swear_word_views.CreateSwearWordUser.as_view(), name='swear-word'),
    path('swear-words', swear_word_views.GetSwearWord.as_view(), name='swear-words')
]
