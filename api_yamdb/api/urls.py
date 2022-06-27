from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (

    UsersViewSet,
    APIGetToken,
    APISignup,
)
app_name = 'api'
router = SimpleRouter()

router.register(
    'users',
    UsersViewSet,
    basename='users'
)
urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]