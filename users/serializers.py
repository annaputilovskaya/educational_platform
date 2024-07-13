from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор платежа.
    """

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """
    Сериализатор пользователя с ограничением информации.
    """

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "phone", "city", "avatar")


class UserDetailSerializer(ModelSerializer):
    """
    Сериализатор пользователя с подробной информацией о платежах.
    """

    payment = PaymentSerializer(source="payment_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
