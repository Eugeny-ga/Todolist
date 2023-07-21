from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.models import Comment
from goals.serializers import CommentCreateSerializer, CommentSerializer


class CommentCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer

class CommentListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["text", "created"]  # Поля, разрешенные для сортировки
    ordering = ["-created"]  # Поле для сортировки по умолчанию
    filterset_fields = ['goal']

    # Вернуть список всех неудаленных (is_deleted) пользователя с запретом на удаление.
    def get_queryset(self):
        return Comment.objects.select_related('user').filter(user=self.request.user)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    # Вернуть список всех комментов данного пользователя
    def get_queryset(self):
        return Comment.objects.select_related('user').filter(user=self.request.user)
