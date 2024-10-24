from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import UserListAPIView, UserCreateAPIView, UserProfileListAPIView, UserProfileDetailAPIView, FriendListCreateAPIView, FriendDetailAPIView, MatchHistoryListCreateAPIView, MatchHistoryDetailAPIView, TournamentListCreateAPIView, TournamentDetailAPIView, SetupTwoFactorView, ConfirmTwoFactorAuthView, TwoFactorSetupTemplateView, TwoFactorConfirmTemplateView, ProtectedMediaView, AcceptedFriendsAPIView, PendingFriendRequestsAPIView


urlpatterns = [
	path("auth/", obtain_auth_token),
	# path("", views.home), TwoFactorTemplateView
	path('users/register/', UserCreateAPIView.as_view(), name='user-register'),
	path('setup-2fa/', SetupTwoFactorView.as_view(), name="setup-2fa"),
	path('confirm-2fa/', ConfirmTwoFactorAuthView.as_view(), name="confirm-2fa"),
	path('setup-2fa-index/', TwoFactorSetupTemplateView.as_view(), name='setup-2fa-index'),
	path('confirm-2fa-index/', TwoFactorConfirmTemplateView.as_view(), name='confirm-2fa-index'),
	path('users/', UserListAPIView.as_view(), name='user-list'),
	path('profiles/', UserProfileListAPIView.as_view(), name='userprofile-list-create'),
	path('profiles/me/', UserProfileDetailAPIView.as_view(), name='userprofile-detail'),
	path('friends/', FriendListCreateAPIView.as_view(), name='friend-list-create'),
	path('friends/accepted/', AcceptedFriendsAPIView.as_view(), name='accepted-friends'),
    path('friends/pending/', PendingFriendRequestsAPIView.as_view(), name='pending-friend-requests'),
	path('friends/<int:pk>/', FriendDetailAPIView.as_view(), name='friend-detail'),
	path('matches/', MatchHistoryListCreateAPIView.as_view(), name='matchhistory-list-create'),
	path('matches/<int:pk>/', MatchHistoryDetailAPIView.as_view(), name='matchhistory-detail'),
	path('tournaments/', TournamentListCreateAPIView.as_view(), name='tournament-list-create'),
	path('tournaments/<int:pk>/', TournamentDetailAPIView.as_view(), name='tournament-detail'),
    path('media/<path:path>', ProtectedMediaView.as_view(), name='protected_media'),
	path('', TemplateView.as_view(template_name='404.html'), name='404'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)