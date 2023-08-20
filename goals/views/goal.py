from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import Goal, GoalStatus
from goals.permissions import GoalPermission
from goals.serializers import GoalCreateSerializer, GoalSerializer


@extend_schema_view(
    post=extend_schema(description='Create new goal', summary='Create goal')
)
class GoalCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


@extend_schema_view(
    get=extend_schema(description="User's goal list", summary='Goals list')
)
class GoalListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields = ["title", "description"]
    ordering = ["title"]
    search_fields = ["title", "description"]
    filterset_class = GoalDateFilter

    # Give away goals that have a category and are not archived.
    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False
        ).exclude(status=GoalStatus.archived)

@extend_schema_view(
    get=extend_schema(description='Get full information about goal', summary='Goal detail'),
    put=extend_schema(description='Update goal information', summary='Update goal'),
    delete=extend_schema(description='Delete goal and goal\'s comments', summary='Delete goal')
)
class GoalDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer
    queryset = Goal.objects.exclude(status=GoalStatus.archived)
    http_method_names = ['get', 'put', 'delete']

    # Instead of deleting the target, we set its status to "archived".
    def perform_destroy(self, instance):
        instance.status = GoalStatus.archived
        instance.save()
        return instance

