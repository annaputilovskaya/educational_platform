from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsOwner, IsUser
from users.serializers import (PaymentSerializer, UserDetailSerializer,
                               UserSerializer)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("paid_at",)

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "retrieve", "destroy"]:
            self.permission_classes = (IsOwner, IsAuthenticated)
        return super().get_permissions()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        print(self.get_object())
        if self.request.user == self.get_object():
            return UserDetailSerializer
        return UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser)


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser)

