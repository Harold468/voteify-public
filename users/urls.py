from users.views import *
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenBlacklistView
)


urlpatterns = [
    path('', ShowUsers.as_view(),name='users'),
    path('api/token/', Validate_USER.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', REFRESH_USER.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/receive_footer_message/', ReceiveFooterMessage.as_view(), name='token_blacklist'),
    path('index/index/', index, name='index'),
    path('<str:id>/', ShowUsers.as_view(),name='users_modify'),
    path('send_verification_code/<str:email>/', send_verification_code.as_view(),name='send_verification_code'),
    path('users/verify_email/',verify_email,name='verify_email'),
    path('users/change_password/',change_password,name='change_password'),
    
    
    
]
