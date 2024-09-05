from django.contrib import admin
from django.urls import path, include
from api.ForgetPassword.view import PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('api.urls')),
    path('auth/',include('security.urls')),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')), # it will show login on top-right corner of api, in which user doesnot need to be staff or admin
    path('pass-reset/<str:temp_token>/', PasswordResetConfirmView.as_view(), name='pass-reset'),
]
