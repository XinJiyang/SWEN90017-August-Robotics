import pytest
from rest_framework.test import APIClient
from rest_framework import status
from DataProcess.models import Client, Hall
from django.urls import reverse
import json
from django.contrib.auth.models import Group

# Create a fixture to ensure the 'admin' group exists.
@pytest.fixture
def setup_group():
    group, created = Group.objects.get_or_create(name='admin')
    return group

# Create a fixture to register an admin user.
@pytest.fixture
def register_admin(setup_group):
    client = APIClient()

    register_data = {
        "username": "admin",
        "password": "123456",
        "privilege": "admin",
        "email": "test@test.com"
    }

    client.post(reverse('register'), data=json.dumps(register_data), content_type='application/json')

# Create a fixture to obtain an authenticated client with the admin user.
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

# Create a fixture to generate a sample client object.
@pytest.fixture
def client_obj():
    return Client.objects.create(
        venue_name="Test Venue",
        region="Test Region",
        email="test@example.com",
        phone="1234567890"
    )

# Create a fixture to generate a sample hall object.
@pytest.fixture
def hall_obj(client_obj):
    return Hall.objects.create(hall="Test Hall", area=500, h_client=client_obj)

# Test to verify the listing of halls.
@pytest.mark.django_db
def test_list_halls(authenticated_client, client_obj, hall_obj):
    url = reverse('hall_list', kwargs={'client_id': client_obj.id})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['hall'] == hall_obj.hall

# Test to verify the creation of a hall.
@pytest.mark.django_db
def test_create_hall(authenticated_client, client_obj, hall_obj):
    url = reverse('hall_list', kwargs={'client_id': client_obj.id})
    hall_data = {
        'hall': 'Expo Center Hall 1',
        'area': "500"
    }
    response = authenticated_client.post(url, data=json.dumps(hall_data), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Hall.objects.count() == 2
    assert Hall.objects.get(id=response.data['id']).hall == 'Expo Center Hall 1'

# Test to verify fetching the details of a hall.
@pytest.mark.django_db
def test_get_hall_detail(authenticated_client, hall_obj):
    url = reverse('hall_detail', kwargs={'hall_id': hall_obj.id})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['hall'] == hall_obj.hall
    assert response.data['area'] == hall_obj.area

# Test to verify the deletion of a hall.
@pytest.mark.django_db
def test_delete_hall(authenticated_client, hall_obj):
    url = reverse('hall_detail', kwargs={'hall_id': hall_obj.id})
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Hall.objects.count() == 0

# Test to verify updating details of a hall.
@pytest.mark.django_db
def test_patch_hall(authenticated_client, hall_obj):
    url = reverse('hall_detail', kwargs={'hall_id': hall_obj.id})
    updated_data = {
        'hall': 'Updated Expo Hall'
    }
    response = authenticated_client.patch(url, data=updated_data)
    assert response.status_code == status.HTTP_200_OK
    hall_obj.refresh_from_db()
    assert hall_obj.hall == 'Updated Expo Hall'
