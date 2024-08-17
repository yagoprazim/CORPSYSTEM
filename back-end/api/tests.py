from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.client import Client

class ClientAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='yagoadmin', password='yago12345')
        self.token = RefreshToken.for_user(self.user).access_token

        self.client_obj = Client.objects.create(
            name="Test",
            cpf="222.222.222-22"
        )
        self.valid_payload = {
            "name": "Yago Prazim",
            "cpf": "000.000.000-00"
        }
        self.invalid_payload = {
            "name": "",
            "cpf": "111.111.111-11"
        }

    def test_create_client_without_authentication(self):
        url = reverse('clients-list')
        response = self.client.post(url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Client.objects.count(), 1)

    def test_create_client(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('clients-list')
        response = self.client.post(url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 2) 
        self.assertEqual(Client.objects.get(name="Yago Prazim").name, "Yago Prazim")

    def test_create_client_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('clients-list')
        response = self.client.post(url, self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Client.objects.count(), 1) 

    def test_delete_client(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('clients-detail', args=[self.client_obj.id])
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0) 

    def test_update_client(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        updated_payload = {
            "name": "Updated Name Test",
            "cpf": "333.333.333-33"
        }
        url = reverse('clients-detail', args=[self.client_obj.id])
        response = self.client.put(url, updated_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.name, "Updated Name Test")
        self.assertEqual(self.client_obj.cpf, "333.333.333-33")