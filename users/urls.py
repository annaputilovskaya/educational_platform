from rest_framework.routers import DefaultRouter, SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet

app_name = UsersConfig.name

router1 = SimpleRouter()
router1.register(r"payment", PaymentViewSet, basename="payment")

router2 = DefaultRouter()
router2.register(r"users", UserViewSet, basename="user")

urlpatterns = []
urlpatterns += router1.urls
urlpatterns += router2.urls
