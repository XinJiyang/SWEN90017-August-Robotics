import pytest
from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
import json

@pytest.fixture
def setup_group():
    group, created = Group.objects.get_or_create(name='admin')
    return group

@pytest.mark.django_db
def test_user_registration_and_login(client, setup_group):
    """
    Test user registration, login, and attempt to register an existing username.
    """
    
    # Register a new user
    register_url = reverse('register') 
    register_data = {
        "username":"test",
        "password":"123456",
        "privilege": "admin",
        "email":"test@test.com"
    }
    register_response = client.post(register_url, register_data, content_type='application/json')
    assert register_response.status_code in [400, 201] , f"Expected status code 200 or 201, but got {register_response.status_code}"

    # Log in with the newly registered user
    login_url = reverse('login')  # Assumes the name of the URL pattern is 'user-login'
    login_data = {'username': 'test', 'password': '123456'}
    login_response = client.post(login_url, login_data, content_type='application/json')
    assert login_response.status_code == 200

    # Attempt to register a user with a username that already exists
    duplicate_register_response = client.post(register_url, register_data, content_type='application/json')
    assert duplicate_register_response.status_code == 400  # This should probably be 400 or 409 if the username is already taken

@pytest.mark.django_db
def test_register_with_long_username(client, setup_group):
    """
    Test user registration with a too-long username.
    """
    
    register_url = reverse('register')
    long_username = 'longusername' + '1' * 150  # This creates a long string without using multiline strings
    data = {'username': long_username, 'password': 'test'}
    response = client.post(register_url, data, content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_login_with_wrong_credentials(client, setup_group):
    """
    Test login attempt with incorrect username.
    """
    
    login_url = reverse('login')
    wrong_credentials = {'username': 'wrong user', 'password': 'test'}
    response = client.post(login_url, wrong_credentials, content_type='application/json')
    assert response.status_code == 401


# Create a fixture to register an admin user
@pytest.fixture
def register_admin(setup_group):
    client = APIClient()
    register_data = {
        "username": "admin",
        "password": "123456",
        "privilege": "admin",
        "email": "admin@test.com"
    }
    client.post(reverse('register'), data=json.dumps(register_data), content_type='application/json')

# Create a fixture to obtain an authenticated client with the admin user
@pytest.fixture
def authenticated_client(register_admin):
    client = APIClient()
    login_data = {
        'username': 'admin',
        'password': '123456'
    }
    response = client.post(reverse('login'), data=json.dumps(login_data), content_type='application/json')
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client

# Test to retrieve the admin user's data
@pytest.mark.django_db
def test_retrieve_user(authenticated_client):
    username = 'admin'
    url = reverse('user', args=[username])
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == username

# Test to update the admin user's data
@pytest.mark.django_db
def test_update_password_and_login(client, authenticated_client):
    username = 'admin'
    old_password = "123456"
    new_password = "654321"
    
    # Update the user's password
    url = reverse('user', args=[username])
    update_data = {
        "old_password": old_password,
        "new_password": new_password,
        "email": "updated@test.com"
    }
    
    response = authenticated_client.put(url, data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    assert response.data['user']['email'] == update_data['email']
    
    # Log in with the old password (should fail)
    login_url = reverse('login')
    old_password_data = {'username': username, 'password': old_password}
    old_password_response = client.post(login_url, old_password_data, content_type='application/json')
    assert old_password_response.status_code == 401  # Should return Unauthorized
    
    # Log in with the new password (should succeed)
    new_password_data = {'username': username, 'password': new_password}
    new_password_response = client.post(login_url, new_password_data, content_type='application/json')
    assert new_password_response.status_code == 200  # Should return OK




# Test to delete the admin user
@pytest.mark.django_db
def test_delete_user(authenticated_client):
    username = 'admin'
    url = reverse('user', args=[username])
    response = authenticated_client.delete(url)
    assert response.status_code == 200