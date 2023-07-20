from django.urls import path

from goals.apps import GoalsConfig
from goals.views.category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.goal import GoalCreateView, GoalListView, GoalDetailView
from goals.views.comment import CommentCreateView, CommentListView, CommentDetailView

urlpatterns = [
    # Category
    path("goal_category/create", GoalCategoryCreateView.as_view()),
    path("goal_category/list", GoalCategoryListView.as_view()),
    path("goal_category/<int:pk>", GoalCategoryView.as_view()),
    # Goal
    path("goal/create", GoalCreateView.as_view()),
    path("goal/list", GoalListView.as_view()),
    path("goal/<int:pk>", GoalDetailView.as_view()),
    # Comment
    path("goal_comment/create", CommentCreateView.as_view()),
    path("goal_comment/list", CommentListView.as_view()),
    path("goal_comment/<int:pk>", CommentDetailView.as_view()),

]