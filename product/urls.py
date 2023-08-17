from django.urls import path
from .views import ProductCreateAPIView, ProductListAPIView, ProductDetailView

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('create/', ProductCreateAPIView.as_view(), name='create-product'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
