from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.models import Comment
from goals.permissions import CommentPermission
from goals.serializers import CommentCreateSerializer, CommentSerializer

@extend_schema_view(
    post=extend_schema(description='Create new comment for goal', summary='Create comment')
)
class CommentCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer
@extend_schema_view(
    get=extend_schema(description="Goal's comments list", summary='Comments list')
)
class CommentListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["text", "created"]
    ordering = ["-created"]
    filterset_fields = ['goal']

    def get_queryset(self):
        return Comment.objects.filter(
            goal__category__board__participants__user=self.request.user)

@extend_schema_view(
    get=extend_schema(description='Get full information about comment', summary='Comment detail'),
    put=extend_schema(description='Update information in comment', summary='Update comment'),
    delete=extend_schema(description='Delete comment', summary='Delete comment')
)
class CommentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [CommentPermission]
    serializer_class = CommentSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        return Comment.objects.select_related('user').filter(
            goal__category__board__participants__user=self.request.user)

