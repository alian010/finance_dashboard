from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LoginPageView, RegisterPageView, RegisterView, MeView

urlpatterns = [
    # JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Register + me
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),

    # HTML pages (tailwind)
    path("login/", LoginPageView.as_view(), name="login_page"),
    path("register-page/", RegisterPageView.as_view(), name="register_page"),
]
