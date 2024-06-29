from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "phone", "city", "avatar")


class UserDetailSerializer(ModelSerializer):
    payment = PaymentSerializer(source="payment_set", many=True, read_only=True)

    class Meta:
        model = User
        # fields = (
        #     "email",
        #     "first_name",
        #     "last_name",
        #     "phone",
        #     "city",
        #     "avatar",
        #     "payment",
        # )
        fields = "__all__"
