
import pytest

from goals.models import Goal, GoalCategory

@pytest.mark.django_db
class TestGoal:
    expected_fields = (
        'id',
        'user',
        'created',
        'updated',
        'title',
        'description',
        'due_date',
        'status',
        'priority',
        'category',
    )

    def test_goals_list(self, authenticated_user: dict):
        """
        Test user get goals list
        Test user get goals with query params (status, priority, category)
        """
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')

        response = client.get('/goals/goal/list')

        assert response.status_code == 200
        assert len(response.data) == 2
        for field in self.expected_fields:
            assert field in response.data[0]
        assert response.data[0].get('user', {}).get('username') == user.username

        category_1 = GoalCategory.objects.filter(user=user)[0]
        category_2 = GoalCategory.objects.filter(user=user)[1]
        [
            Goal.objects.create(title=f'To do {i}', user=user, category=category_1, status=2, priority=3)
            for i in range(8)
        ]
        [
            Goal.objects.create(title=f'In progress {i}', user=user, category=category_2, status=3, priority=4)
            for i in range(5)
        ]
        response = client.get('/goals/goal/list?limit=10')
        results = response.data.get('results')

        assert len(results) == 10
        assert response.data.get('count') == 15

        response = client.get('/goals/goal/list?status__in=2')
        assert len(response.data) == 8

        response = client.get('/goals/goal/list?priority__in=4')
        assert len(response.data) == 5

        response = client.get(f'/goals/goal/list?category__in={category_1.id}')
        assert len(response.data) == 9

    def test_category_get_by_id(self, authenticated_user: dict):
        """Test user get goal by id"""
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')
        goal = Goal.objects.filter(user=user).first()

        response = client.get(f'/goals/goal/{goal.id}')

        assert response.status_code == 200
        for field in self.expected_fields:
            assert field in response.data
        assert response.data.get('user', {}).get('username') == user.username

    def test_goal_create_update_delete(self, authenticated_user: dict):
        """
        Test user create a goal
        Test user update the goal
        Test user delete the goal
        """
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')
        category = GoalCategory.objects.filter(user=user).first()

        response = client.post(
            '/goals/goal/create',
            {'title': 'New goal', 'category': category.id},
            content_type='application/json',
        )

        assert response.status_code == 201
        assert response.data.get('title') == 'New goal'
        assert response.data.get('category') == category.id

        goal_id = response.data.get('id')

        response = client.put(
            f'/goals/goal/{goal_id}',
            {'title': 'Goal title updated', 'category': category.id},
            content_type='application/json',
        )
        assert response.status_code == 200
        assert response.data.get('title') == 'Goal title updated'

        response = client.delete(f'/goals/goal/{goal_id}')
        assert response.status_code == 204
