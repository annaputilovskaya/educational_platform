from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    UserListAPIView

app_name = UsersConfig.name

router1 = SimpleRouter()
router1.register(r"payment", PaymentViewSet, basename="payment")

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='profile'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='delete'),
    path('', UserListAPIView.as_view(), name='list'),
]
urlpatterns += router1.urls
