
import pytest
from django.test import Client
from core.models import User


@pytest.mark.django_db
class TestCoreAuthentication:
    def test_core_signup(self) -> None:
        """Test user sign up"""
        client = Client()
        response = client.post(
            '/core/signup',
            {'username': 'test_user', 'password': 'Pswrd1456623', 'password_repeat': 'Pswrd1456623'},
            content_type='application/json',
        )
        expected_response = {'id': 1, 'username': 'test_user', 'email': '', 'first_name': '', 'last_name': ''}
        assert response.status_code == 201
        assert response.data == expected_response

    def test_core_login(self, authenticated_user: dict) -> None:
        """Test user login"""
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')
        password = authenticated_user.get('password')

        response = client.post(
            '/core/login',
            {'username': user.username, 'password': password},
            content_type='application/json',
        )
        expected_response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        assert response.status_code == 200
        assert response.data == expected_response

    def test_core_profile(self, authenticated_user: dict) -> None:
        """
        Test for user profile retrieval,
        Test for user profile update,
        Test for user profile patch (with validation error for username)"""
        client = authenticated_user.get('client')
        user = authenticated_user.get('user')

        response = client.get('/core/profile')
        expected_response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        assert response.status_code == 200
        assert response.data == expected_response

        changes_data = {
            'username': 'changed_name',
            'email': 'test_email@wrong.me',
            'first_name': 'Name',
            'last_name': 'Surname',
        }

        # Check PUT method with user data changing
        response = client.put('/core/profile', changes_data, content_type='application/json')
        changes_data['id'] = user.id

        assert response.status_code == 200
        assert response.data == changes_data

        # Check PATCH method with username already exists bad request
        User.objects.create(username='user_exists', password='testPassword')
        response = client.patch('/core/profile', {'username': 'user_exists'}, content_type='application/json')

        assert response.status_code == 400
        assert 'Пользователь с таким именем уже существует.' in response.data.get('username')[0]

    def test_core_update_password(self, authenticated_user: dict) -> None:
        """Test user update password"""
        client = authenticated_user.get('client')
        password = authenticated_user.get('password')

        response = client.put(
            '/core/update_password',
            {'old_password': password, 'new_password': 'new_password1234'},
            content_type='application/json',
        )
        assert response.status_code == 200
        assert response.data == {}
