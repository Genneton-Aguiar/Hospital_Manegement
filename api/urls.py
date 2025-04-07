
from rest_framework import routers
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename = 'users')
router.register('doctor', DoctorsViewSet, basename = 'doctor')
router.register('patient', PatientsViewSet, basename = 'patient')
router.register('appointment', AppointmentsViewSet, basename = 'appointment')
router.register('payments', PaymentsViewSet, basename = 'payments')
router.register('admlist', AdminListViewSet, basename = 'admlist')
router.register('doclist', DoctorsListViwSet, basename = 'doclist')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name = 'token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name = 'token_verify'),
]

