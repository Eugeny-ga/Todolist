from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import Goal, GoalStatus
from goals.permissions import GoalPermission
from goals.serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer

class GoalListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["title", "description"]  # Поля, разрешенные для сортировки
    ordering = ["title"]  # Поле для сортировки по умолчанию
    search_fields = ["title", "description"]
    filterset_class = GoalDateFilter

    #Отдаем цели, у которых есть категория и которые не в архиве.
    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False
        ).exclude(status=GoalStatus.archived)


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer
    queryset = Goal.objects.exclude(status=GoalStatus.archived)

    # Вместо удаления цели, устанавливаем его статус "в архиве".
    def perform_destroy(self, instance):
        instance.status = GoalStatus.archived
        instance.save()
        return instance

