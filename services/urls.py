# from django.urls import path
# from .views import home_view
# from django.urls import path
# from .views import home_view, register, verify_otp, service_create, service_detail, service_update, service_delete, service_list
#
# urlpatterns = [
#     path('', home_view, name='home'),
#     path('register/', register, name='register'),
#     path('verify_otp/', verify_otp, name='verify_otp'),
#     path('services/', service_list, name='service_list'),
#     path('services/create/', service_create, name='service_create'),
#     path('services/<int:pk>/', service_detail, name='service_detail'),
#     path('services/<int:pk>/update/', service_update, name='service_update'),
#     path('services/<int:pk>/delete/', service_delete, name='service_delete'),
# ]
from django.urls import path
from.views import home_view1
from .views import send_test_email
from .views import register_user, confirm_otp
from .views import login_view    #home_view
# from .views import create_service
# from .views import
from .views import create_service, service_detail, update_service, delete_service,list_services
from  .views import subscription_view,payment_callback

urlpatterns = [
    # path('', home_view, name='home'),
    path('send-email/', send_test_email, name='send_email'),
    path('register/', register_user, name='register'),  # URL for registration page
    path('confirm-otp/', confirm_otp, name='confirm_otp'),  # URL for OTP confirmation page
    path('login/', login_view, name='login'),  # URL for the login page
    path('home/', home_view1, name='home'),  # URL for the home page
    # path('register2/', register_view, name='register'),  # URL for the registration page

    # path('create/',create_service, name='create_service'),
    # path('service-list/',service_list, name='service_list'),

    path('create-service/', create_service, name='create_service'),
    path('<int:pk>/', service_detail, name='service_detail'),
    path('<int:pk>/edit/', update_service, name='update_service'),
    path('<int:pk>/delete/', delete_service, name='delete_service'),
    path('',list_services, name='service_list'),


     path('subscribe/<int:service_id>/',subscription_view, name='subscription'),

     path('payment/callback/', payment_callback, name='payment_callback'),
]




