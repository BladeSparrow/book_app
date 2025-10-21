from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView,
    RegisterPageView, LoginPageView, PublicPageView, ProtectedPageView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('pages/register/', RegisterPageView.as_view(), name='register_page'),
    path('pages/login/', LoginPageView.as_view(), name='login_page'),
    path('pages/public/', PublicPageView.as_view(), name='public_page'),
    path('pages/protected/', ProtectedPageView.as_view(), name='protected_page'),
]
