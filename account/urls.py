from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('password_reset/', UserPasswordResetView.as_view(),
         name='user_password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete/', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('follow/<int:user_id>/',
         UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/',
         UserUnfollowView.as_view(), name='user_unfollow'),
    path('edit_user', EditUserView.as_view(), name='edit_user'),
]
