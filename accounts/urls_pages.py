from django.urls import path
from .views import RegisterPageView, LoginPageView, PublicPageView, ProtectedPageView

app_name = 'accounts_pages'

urlpatterns = [
    path('pages/register/', RegisterPageView.as_view(), name='register_page'),
    path('pages/login/', LoginPageView.as_view(), name='login_page'),
    path('pages/public/', PublicPageView.as_view(), name='public_page'),
    path('pages/protected/', ProtectedPageView.as_view(), name='protected_page'),
]
