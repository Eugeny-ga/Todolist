from django.db import transaction
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from goals.models import GoalCategory, GoalStatus, Goal
from goals.permissions import GoalCategoryPermission
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["title", "created"]  # Поля, разрешенные для сортировки
    ordering = ["title"]  # Поле для сортировки по умолчанию
    search_fields = ["title"]

    # Вернуть список всех категорий пользователя с запретом на удаление.
    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            board__participants__user=self.request.user, is_deleted=False)

class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategorySerializer
    queryset = GoalCategory.objects.select_related('user').exclude(is_deleted=True)

    # Вместо удаления категории, устанавливаем его параметр is_deleted=True.
    # Всем связанным целям меняем статус на архивный.
    # Оборачиваем в транзакцию.
    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            Goal.objects.filter(category=instance.id).update(status=GoalStatus.archived)


