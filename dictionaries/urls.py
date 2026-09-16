from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import RefbookListView, RefbookElementsView, RefbookCheckElementView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('refbooks/', RefbookListView.as_view(), name='refbook-list'),
    path('refbooks/<int:pk>/elements', RefbookElementsView.as_view(), name='refbook-elements'),
    path('refbooks/<int:pk>/check_element', RefbookCheckElementView.as_view(), name='refbook-check-element'),
]
