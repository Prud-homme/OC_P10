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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import RegisterView
from softdesk_api.views import ProjectAPIView, IssueAPIView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterView.as_view(), name='auth_register'),

    path('projects/', ProjectAPIView.as_view(), name='projects'),
    path('projects/<int:project_id>/', ProjectAPIView.as_view(), name='projects-details'),
    #path('projects/<int:project_id>/users/',),
    #path('projects/<int:project_id>/users/<int:user_id>/',),
    path('projects/<int:project_id>/issues/', IssueAPIView.as_view(), name='issues'),
    path('projects/<int:project_id>/issues/<int:issue_id>/', IssueAPIView.as_view(), name='issues-details'),
    #path('projects/<int:project_id>/issues/<int:issue_id>/comments/',),
    #path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/',),
]
