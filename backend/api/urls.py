
from django.contrib import admin
from django.urls import path,include
from api.Permission import view as permissionView
from api.Role import view as roleView
from api.User import view as userView
from api.TestAPI import view as TestView
from api.Address import view as AddressView


from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router=routers.DefaultRouter()
router.register(r'user',userView.UserViewset, basename='user'),
router.register(r'role',roleView.RoleViewset, basename='role'),
router.register(r'permission', permissionView.PermissionViewset, basename='permission'),
router.register(r'test', TestView.TestViewset, basename='test'),
router.register(r'address',AddressView.AddressViewset,basename='address'),


# Create a schema view for drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Placeholder API",
        default_version='v1',
        description="Your API Description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('',include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]