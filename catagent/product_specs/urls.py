from django.urls import path
from .views import GetSpecsView, ImageSpecsView

urlpatterns = [
    path('api/get-specs/', GetSpecsView.as_view(), name='get-specs'),
    path('api/image-specs/', ImageSpecsView.as_view(), name='image-specs')
]
