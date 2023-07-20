
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, GoalStatus, Goal, Comment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if value.is_deleted:
            raise NotFound("Category not found")
        return value

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = GoalCategorySerializer

    #Пользовательская проверка
    # на уровне полей, добавив validate_<field_name>
    # методы в свой Serializer подкласс.
    #Эти методы принимают единственный аргумент,
    # который является значением поля, требующим проверки.
    def validate_category(self, value: GoalCategory):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")
        # Проверяем, что пользователь - владелец
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    category = GoalCategorySerializer
    due_date = serializers.DateField(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, value: Goal):
        if value.status == GoalStatus.archived:
            raise NotFound("Goal not exist")
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")
        return value

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
