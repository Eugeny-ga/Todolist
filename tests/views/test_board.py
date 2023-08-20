from typing import OrderedDict
import pytest
from goals.models import Board, BoardParticipant

@pytest.mark.django_db
class TestBoards:
    expected_fields = ['id', 'created', 'updated', 'title', 'is_deleted']

    def test_board_list(self, authenticated_user: dict):
        """Test user get boards list"""
        client = authenticated_user.get('client')
        response = client.get('/goals/board/list')

        assert response.status_code == 200
        for field in self.expected_fields:
            assert field in response.data[0]

    def test_board_get_by_id(self, authenticated_user: dict):
        """Test user get the board"""
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')
        board = Board.objects.filter(participants__user=user).first()

        response = client.get(f'/goals/board/{board.id}')
        expected_fields = self.expected_fields + ['participants']

        assert response.status_code == 200
        for field in expected_fields:
            assert field in response.data.keys()
        assert isinstance(response.data.get('participants')[0], OrderedDict)

    def test_board_create_update_delete(self, authenticated_user: dict, users: list):
        """
        Test user create a board
        Test user update the board with other participants
        Test user delete the board
        """
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')

        response = client.post(
            '/goals/board/create',
            {'title': 'New board'},
            content_type='application/json',
        )

        assert response.status_code == 201
        for field in self.expected_fields:
            assert field in response.data

        board = Board.objects.filter(participants__user=user).first()
        changes_data = {
            'participants': [{'role': 2, 'user': users[0].username}, {'role': 3, 'user': users[1].username}],
            'title': 'Changed board',
            'is_deleted': False,
        }
        response = client.put(f'/goals/board/{board.id}', changes_data, content_type='application/json')
        participants = response.data.get('participants')
        user1_data = participants[0]
        user2_data = participants[1]
        user3_data = participants[2]

        assert response.status_code == 200
        assert response.data['title'] == 'Changed board'
        assert user1_data.get('user') == user.username
        assert user1_data.get('role') == BoardParticipant.Role.owner
        assert user2_data.get('user') == users[0].username
        assert user2_data.get('role') == BoardParticipant.Role.writer
        assert user3_data.get('user') == users[1].username
        assert user3_data.get('role') == BoardParticipant.Role.reader

        response = client.delete(f'/goals/board/{board.id}')
        assert response.status_code == 204
