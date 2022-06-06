from authentication.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

from rest_framework.generics import CreateAPIView
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer