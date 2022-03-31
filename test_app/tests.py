from django.urls import reverse
from operator import mod
from django.contrib.auth.models import User
from rest_framework import status
from knox.models import AuthToken
from rest_framework.test import APITestCase
from .models import *

class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
                "username": "test1",
                "email": "test@test.com",
                "password": "test"
                }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestSetUp(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="some_password")
        self.token = AuthToken.objects.create(self.user)[1]
        self.api_authentication()
        return super().setUp()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token)

class EmployeeApiViewTest(TestSetUp):
    emp_url = reverse('employees')

    def test_employee_create_authenticated(self):
        data = {"firstname":"test", "lastname":"test"}
        test_response = {"employee_id": 1,"firstname": "test","lastname": "test"}
        response = self.client.post(self.emp_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_response)
    
    def test_employee_list_authenticated(self):
        employees.objects.create(firstname='test', lastname='test')
        test_response = [{'employee_id': 1, 'firstname': 'test', 'lastname': 'test'}]
        response = self.client.get(self.emp_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_response)

    def test_employee_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

class RoomViewSetTestCase(TestSetUp):
    def test_room_create_authenticated(self):
        data = {"room_number":"A4"}
        test_response = {"room_id": 1,"room_number": "A4"}
        response = self.client.post('/api/rooms/', data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_response)
    
    def test_room_list_authenticated(self):
        rooms.objects.create(room_number="A4")
        test_response = [{"room_id": 1,"room_number": "A4"}]
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), test_response)


class DeleteReservationApiTest(TestSetUp):
    def test_reservation_delete_error(self):
        response = self.client.get('/api/delete_reservation/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReservationApiTest(TestSetUp):
    def test_reservation_create(self):
        data = {
                "start_time": "2022-03-25T11:08:59Z",
                "end_time": "2022-03-25T11:09:01Z",
                "title": "Test",
                "availability": True,
                "room_id": 1,
                "organizer": 1
                }
        response = self.client.post('/api/reservations/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test')