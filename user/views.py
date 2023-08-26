# user/views.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from customer.models import Customer
from franchise.models import Franchise
from inventory.models import Inventory
from product.models import Product
from sales.models import Sales
from .filters import CustomerFilter
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer, \
    AdminChangePasswordSerializer, UserUpdateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .permissions import IsAdminUser, IsUser
from django.utils.encoding import force_bytes
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import check_password


class NoPagination(PageNumberPagination):
    page_size = None


class CustomUserCreateView(CustomResponseMixin, generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'User with this Phone number already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class CustomUserListView(CustomResponseMixin, generics.ListAPIView):
    pagination_class = NoPagination
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomerFilter
    search_fields = ['first_name', 'email', 'user_type']
    ordering_fields = ['first_name', 'created_at']


class CustomUserDetailView(CustomResponseMixin, generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    lookup_field = 'id'

    # user/views.py


class CustomTokenObtainPairView(CustomResponseMixin, TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    pass


class ChangePasswordView(CustomResponseMixin, APIView):
    permission_classes = [IsUser]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_new_password = serializer.validated_data['confirm_new_password']
        if not check_password(old_password, user.password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_new_password:
            return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_password.strip()) < 8:
            return Response({'error': 'Password must be minimum 8 character long.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password successfully changed.'}, status=status.HTTP_200_OK)


class AdminChangePasswordView(CustomResponseMixin, APIView):
    permission_classes = [IsAdminUser]
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = AdminChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = CustomUser.objects.get(serializer.validated_data['email'])
        except CustomUser.DoesNotExist:
            return Response({"error": 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        new_password = serializer.validated_data['new_password']
        confirm_new_password = serializer.validated_data['confirm_new_password']
        if new_password != confirm_new_password:
            return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_password.strip()) < 8:
            return Response({'error': 'Password must be minimum 8 character long.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password successfully changed.'}, status=status.HTTP_200_OK)


class ForgotPasswordView(CustomResponseMixin, APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            send_password_reset_email(user)
            return Response({'message': 'Password reset email sent.', 'status': 1})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.', 'status': 0}, status=400)


def send_password_reset_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"http://your-domain/reset-password/{uid}/{token}/"

    subject = "Password Reset"
    message = render_to_string('reset_password_email.html', {
        'user': user,
        'reset_link': reset_link,
    })
    from_email = "your-email@example.com"
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


class TotalCountsView(CustomResponseMixin, APIView):
    permission_classes = [IsUser]

    def get(self, request):
        if self.request.user.user_type == 'admin':
            user_count = CustomUser.objects.count()
            franchise_count = Franchise.objects.count()
            sales_count = Sales.objects.count()
            customer_count = Customer.objects.count()
            product_count = Product.objects.count()
            response_data = {
                "user_count": user_count,
                "franchise_count": franchise_count,
                "sales_count": sales_count,
                "customer_count": customer_count,
                "product_count": product_count,

            }
            return Response(response_data, status=status.HTTP_200_OK)
        elif self.request.user.user_type == 'franchise':
            sales_count = Sales.objects.filter(franchise=self.request.user.franchise).count()
            customer_count = Customer.objects.count()
            product_count = Inventory.objects.filter(franchise=self.request.user.franchise).count()
            response_data = {
                "sales_count": sales_count,
                "customer_count": customer_count,
                "product_count": product_count,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid access"}, status=status.HTTP_403_FORBIDDEN)


class CurrentUserView(CustomResponseMixin, generics.RetrieveAPIView):
    permission_classes = [IsUser]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.get(id=self.request.user.id)


class CustomUserUpdateView(CustomResponseMixin, generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')

            if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(phone_number=phone_number).exclude(id=user_id).exists():
                return Response({'error': 'User with this Phone number already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer.save(username=email)
            return Response({'message': 'User details successfully updated.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



