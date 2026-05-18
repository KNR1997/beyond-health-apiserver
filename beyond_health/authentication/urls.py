from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from beyond_health.authentication.views import SignupView, SigninView, CreateAdminView, MeView, ChangePasswordEndpoint, \
    LogoutView, InitializeAdminView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', SignupView.as_view(), name='signup'),
    path('token', SigninView.as_view(), name='token'),
    path('create-admin/', CreateAdminView.as_view(), name='create_admin'),
    path('me', MeView.as_view(), name='me'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change-password', ChangePasswordEndpoint.as_view(), name='change-password'),
    path('init-admin/', InitializeAdminView.as_view(), name='initialize_admin'),

]
