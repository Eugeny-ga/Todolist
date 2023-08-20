from django.db import transaction
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions, filters

from goals.models import Board, Goal, GoalStatus, BoardParticipant
from goals.permissions import BoardPermission
from goals.serializers import BoardSerializer, BoardWithParticipantSerializer


@extend_schema_view(
    post=extend_schema(description='Create new board for categories', summary='Create board')
)
class BoardCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(
                user=self.request.user, board=board)


@extend_schema_view(
    get=extend_schema(description="User's board list", summary='Board list')
)
class BoardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user).exclude(is_deleted=True)


@extend_schema_view(
    get=extend_schema(description='Get full information about board', summary='Board detail'),
    put=extend_schema(description='Update information or participants in board', summary='Update board'),
    delete=extend_schema(description='Delete board and board\'s categories and goals', summary='Delete board')
)
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardWithParticipantSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=GoalStatus.archived)
        return instance
