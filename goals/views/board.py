from django.db import transaction
from rest_framework import generics, permissions, filters

from goals.models import Board, Goal, GoalStatus, BoardParticipant
from goals.permissions import BoardPermission
from goals.serializers import BoardSerializer, BoardWithParticipantSerializer


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(
                user=self.request.user, board=board)


class BoardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user).exclude(is_deleted=True)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardWithParticipantSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=GoalStatus.archived)
        return instance
