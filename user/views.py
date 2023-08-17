# user/views.py
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from Bakery_Management_System.custom_mixin_response import CustomResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .filters import CustomerFilter
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .permissions import IsAdminUser, IsUser
from django.utils.encoding import force_bytes
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import check_password

class NoPagination(PageNumberPagination):
    page_size = None
class CustomUserCreateView(CustomResponseMixin,generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number=request.data.get('phone_number')
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(phone_number=phone_number).exists():
             return Response({'error': 'User with this Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)


class CustomUserListView(CustomResponseMixin,generics.ListAPIView):
    pagination_class = NoPagination
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomerFilter
    search_fields = ['first_name', 'email', 'user_type']
    ordering_fields = ['first_name', 'created_at']


class CustomUserDetailView(CustomResponseMixin,generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

    # user/views.py


class CustomTokenObtainPairView(CustomResponseMixin,TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    pass


class ChangePasswordView(APIView):
    permission_classes = [IsUser]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_new_password = serializer.validated_data['confirm_new_password']
        print(user.password)
        if not check_password(old_password, user.password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_new_password:
            return Response({'error': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password successfully changed.'}, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(user)
            return Response({'message': 'Password reset email sent.','status':1})
        except User.DoesNotExist:
            return Response({'error': 'User not found.','status':0}, status=400)


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

