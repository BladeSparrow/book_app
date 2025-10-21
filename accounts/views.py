import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import exceptions as drf_exceptions
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer

logger = logging.getLogger('accounts')


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info('RegisterView POST called')
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except Exception as e:
                logger.exception('Error saving user: %s', e)
                return Response({'detail': 'Could not create user. Username or email may already be in use.'}, status=status.HTTP_400_BAD_REQUEST)
            logger.info('User registered: %s', user.username)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        logger.warning('Register validation failed: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """Override to return plain-text message on auth failure."""
        try:
            return super().post(request, *args, **kwargs)
        except drf_exceptions.ValidationError as exc:
            detail = exc.detail
            
            message = None
            if isinstance(detail, dict):
                for key in ('detail', 'non_field_errors'):
                    if key in detail:
                        val = detail[key]
                        if isinstance(val, (list, tuple)) and val:
                            message = str(val[0])
                        else:
                            message = str(val)
                        break
                if message is None:
                    try:
                        first = next(iter(detail.values()))
                        message = str(first[0]) if isinstance(first, (list, tuple)) else str(first)
                    except Exception:
                        message = str(detail)
            elif isinstance(detail, (list, tuple)) and detail:
                message = str(detail[0])
            else:
                message = str(detail)
            return HttpResponse(message, status=401, content_type='text/plain; charset=utf-8')


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        logger.info('Logout requested by user: %s', request.user.username)
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            logger.info('Logout called without refresh token')
            return Response(status=status.HTTP_205_RESET_CONTENT)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info('Refresh token blacklisted')
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            if 'blacklist' in str(e).lower():
                logger.info('Logout requested for already-blacklisted token')
                return Response(status=status.HTTP_205_RESET_CONTENT)
            logger.exception('TokenError during logout: %s', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception('Error during logout: %s', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterPageView(View):
    def get(self, request):
        
        access = request.COOKIES.get('access')
        if access:
            try:
                UntypedToken(access)
                return HttpResponseRedirect('/accounts/pages/protected/')
            except Exception:
                pass
        return render(request, 'accounts/register.html')


class LoginPageView(View):
    def get(self, request):
        
        access = request.COOKIES.get('access')
        if access:
            try:
                UntypedToken(access)
                next_url = request.GET.get('next') or '/accounts/pages/public/'
                return HttpResponseRedirect(next_url)
            except Exception:
                pass
        return render(request, 'accounts/login.html')


class PublicPageView(View):
    def get(self, request):
        return render(request, 'accounts/public.html')


class ProtectedPageView(View):
    def get(self, request):
        
        access = request.COOKIES.get('access')
        if not access:
            login_url = '/accounts/pages/login/'
            return redirect(f"{login_url}?next={request.path}")
        try:
            UntypedToken(access)
        except Exception:
            login_url = '/accounts/pages/login/'
            return redirect(f"{login_url}?next={request.path}")
        
        return render(request, 'accounts/protected.html', {'username': request.COOKIES.get('username')})

