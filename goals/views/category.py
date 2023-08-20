from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from goals.models import GoalCategory, GoalStatus, Goal
from goals.permissions import GoalCategoryPermission
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


@extend_schema_view(
    post=extend_schema(description='Create new categories for goals', summary='Create category')
)
class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer

@extend_schema_view(
    get=extend_schema(description="User's categories list", summary='Categories list')
)
class GoalCategoryListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["board"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    # Return a list of all user categories with a ban on deletion.
    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            board__participants__user=self.request.user, is_deleted=False)
@extend_schema_view(
    get=extend_schema(description='Get full information about category', summary='Category detail'),
    put=extend_schema(description='Update category information', summary='Update category'),
    delete=extend_schema(description='Delete category and category\'s goals', summary='Delete category')
)
class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCategoryPermission]
    serializer_class = GoalCategorySerializer
    queryset = GoalCategory.objects.select_related('user').exclude(is_deleted=True)
    http_method_names = ['get', 'put', 'delete']

    # Instead of deleting the category, set its parameter is_deleted=True.
    # We change the status to archived for all related goals.
    # Wrapping it in a transaction.
    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            Goal.objects.filter(category=instance.id).update(status=GoalStatus.archived)


