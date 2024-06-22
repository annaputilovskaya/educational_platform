from rest_framework.routers import SimpleRouter, DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router1 = SimpleRouter()
router1.register(r'payment', PaymentViewSet, basename='payment')

router2 = DefaultRouter()
router2.register(r'users', UserViewSet, basename='user')

urlpatterns = []
urlpatterns += router1.urls
urlpatterns += router2.urls
