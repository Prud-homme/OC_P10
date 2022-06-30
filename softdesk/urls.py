"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path


from authentication.views import (
    RegisterView,
    UserInformationsView,
    TokenObtainPairView,
    TokenRefreshView,
)
from softdesk_api.views import (
    CommentAPIView,
    ContributorAPIView,
    IssueAPIView,
    ProjectAPIView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterView.as_view(), name="auth_register"),
    path("account/", UserInformationsView.as_view(), name="account_info"),
    path("projects/", ProjectAPIView.as_view(), name="projects"),
    path(
        "projects/<int:project_id>/", ProjectAPIView.as_view(), name="projects-details"
    ),
    path(
        "projects/<int:project_id>/users/",
        ContributorAPIView.as_view(),
        name="contributors-list",
    ),
    path(
        "projects/<int:project_id>/users/<int:user_id>/",
        ContributorAPIView.as_view(),
        name="contributors",
    ),
    path("projects/<int:project_id>/issues/", IssueAPIView.as_view(), name="issues"),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/",
        IssueAPIView.as_view(),
        name="issues-details",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/",
        CommentAPIView.as_view(),
        name="comments",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/",
        CommentAPIView.as_view(),
        name="comments-details",
    ),
]
