from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .permissions import IsUser
from .serializers import UserCommonSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для Пользователя"""

    model = User
    queryset = User.objects.all()

    def get_serializer_class(self):
        if (
            self.action in ("retrieve", "update", "partial_update", "destroy")
            and self.request.user.email == self.get_object().email
        ):
            return UserSerializer
        return UserCommonSerializer

    def get_permissions(self):
        """Устанавливает права на действия пользователя."""

        if self.action in ("update", "partial_update", "destroy"):
            permission_classes = [IsAuthenticated, IsUser]
        elif self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
