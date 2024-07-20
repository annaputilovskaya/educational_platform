from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsOwner, IsUser
from users.serializers import (PaymentSerializer, UserDetailSerializer,
                               UserSerializer)
from users.services import (choose_material, create_stripe_price,
                            create_stripe_product, create_stripe_session)


class PaymentViewSet(ModelViewSet):
    """
    Контроллер платежа.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("paid_at",)

    def get_permissions(self):
        """
        Получает права доступа для разных действий.
        """
        if self.action in ["create", "list"]:
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "retrieve", "destroy"]:
            self.permission_classes = (IsOwner, IsAuthenticated)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Сохраняет платеж и создает сессию в страйпе для безналичной оплаты.
        """
        payment = serializer.save(user=self.request.user)
        material = choose_material(payment)
        if payment.payment_method == "TRANSFER":

            # Создание платежа в страйпе.
            product = create_stripe_product(material)
            price = create_stripe_price(payment.amount, product)
            session_id, payment_link = create_stripe_session(price)

            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
        else:
            # Оплата наличными.
            payment.save()


class UserCreateAPIView(CreateAPIView):
    """
    Контроллер регистрации пользователя.
    """

    serializer_class = UserDetailSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """
    Контроллер списка пользователей.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер детального просмотра пользователя.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Проверяет, какой объем информации о пользователе может просматривать текущий пользователь.
        """
        if self.request.user == self.get_object():
            return UserDetailSerializer
        return UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """
    Контроллер изменения информации о пользователе.
    """

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser)


class UserDestroyAPIView(DestroyAPIView):
    """
    Контроллер удаления пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser)
