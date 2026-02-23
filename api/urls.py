# backend/api/urls.py
# Main URL configuration for API endpoints
from django.contrib import admin
from django.urls import path,include
# Import views for different modules
from api.Permission import view as permissionView
from api.Role import view as roleView
from api.User import view as userView
from api.ChangeMyPassword.view import ChangeMyPasswordView
from api.ForgetPassword.view import PasswordResetRequestView
from api.IsSuperUser.view import CheckUserType
from api.CreateUser import views as createUserViews

# Import HR module views
from api.Department.view import DepartmentViewSet
from api.AttendanceStatus.view import AttendanceStatusViewSet
from api.Attendance.view import AttendanceViewSet
from api.Leave.view import LeaveViewSet
from api.YearMaster.view import YearMasterViewSet
from api.salary.view import SalaryViewSet
from api.CustomAPI.adminDashboard import AdminDashboardAPIView

# REST Framework and Swagger imports
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi




# Router configuration for ViewSets
router=routers.DefaultRouter()
# User management endpoints
router.register(r'user',userView.UserViewset, basename='user')
router.register(r'role',roleView.RoleViewset, basename='role')
router.register(r'permission', permissionView.PermissionViewset, basename='permission')

# HR module endpoints
router.register(r'department', DepartmentViewSet, basename='department')
router.register(r'attendanceStatus', AttendanceStatusViewSet, basename='attendanceStatus')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'leave', LeaveViewSet, basename='leave')
router.register(r'yearmaster', YearMasterViewSet, basename='yearmaster')
router.register(r'salary', SalaryViewSet, basename='salary')




# Swagger/OpenAPI schema configuration for API documentation
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
    permission_classes=(permissions.AllowAny,),  # Public access to API docs
)

urlpatterns = [
    # Router URLs for ViewSets
    path('',include(router.urls)),
    # API documentation endpoints
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication and user management endpoints
    path('changeMyPassword/', ChangeMyPasswordView.as_view(), name='changeMyPassword'),
    path('passwordReset/', PasswordResetRequestView.as_view(), name='passwordResetRequest'),
    # path('pass-reset/<str:temp_token>/', PasswordResetConfirmView.as_view(), name='pass-reset'),  # put it in security(auth) app's urls
    path('isSuperUser/', CheckUserType.as_view(), name='isSuperUser'),
    path('createUser/', createUserViews.CreateUserAPI.as_view(), name='create-user'),
    # Dashboard endpoint
    path('adminDashboard/', AdminDashboardAPIView.as_view(), name='admin-dashboard'),

]