
import pytest

from goals.models import Board, GoalCategory

@pytest.mark.django_db
class TestCategory:
    expected_fields = ('id', 'user', 'board', 'created', 'updated', 'title', 'is_deleted')

    def test_category_list(self, authenticated_user: dict):
        """Test user get categories list"""
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')

        response = client.get('/goals/goal_category/list')

        assert response.status_code == 200
        assert len(response.data) == 2
        for field in self.expected_fields:
            assert field in response.data[0]
        assert response.data[0].get('user').get('username') == user.username

    def test_category_get_by_id(self, authenticated_user: dict):
        """Test user get category by id"""
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')
        category = GoalCategory.objects.filter(user=user).first()

        response = client.get(f'/goals/goal_category/{category.id}')

        assert response.status_code == 200
        for field in self.expected_fields:
            assert field in response.data
        assert response.data.get('user', {}).get('username') == user.username

    def test_category_create_update_delete(self, authenticated_user: dict):
        """
        Test user create a category
        Test user update the category
        Test user delete the category
        """
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')
        board = Board.objects.filter(participants__user=user).first()

        response = client.post(
            '/goals/goal_category/create',
            {'title': 'New category', 'board': board.id},
            content_type='application/json',
        )

        assert response.status_code == 201
        assert response.data.get('title') == 'New category'
        assert response.data.get('board') == board.id


        category_id = response.data.get('id')

        response = client.put(
            f'/goals/goal_category/{category_id}',
            {'title': 'Title updated', 'board': board.id},
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.data.get('title') == 'Title updated'

        response = client.delete(f'/goals/goal_category/{category_id}')
        assert response.status_code == 204

        response = client.get(f'/goals/goal_category/{category_id}')
        assert response.status_code == 404

