from django.urls import path
from .views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView, CustomerByPhoneNumberView

urlpatterns = [
    path('', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'),
    path('phone/<str:phone_number>/', CustomerByPhoneNumberView.as_view(), name='customer-by-phone'),

]
