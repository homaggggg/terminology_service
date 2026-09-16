import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from .models import Dictionary, DictionaryVersion, DictionaryElement

from django.test import TestCase

# Create your tests here.

@pytest.mark.django_db
class TestRefbooksAPI:
    
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.client = APIClient()
        
        self.dict_1 = Dictionary.objects.create(code="MS1", name="Справочник заболеваний")
        
        self.version_1 = DictionaryVersion.objects.create(
            dictionary=self.dict_1,
            version="1.0",
            start_date=timezone.datetime(2022, 10, 1).date()
        )
        
        self.elem_1 = DictionaryElement.objects.create(version=self.version_1, code="J00", value="ОРИ")
        self.elem_2 = DictionaryElement.objects.create(version=self.version_1, code="J01", value="Синусит")

    def test_get_refbooks_list_without_date(self):
        """Проверка получения списка всех справочников"""
        url = reverse('refbook-list')
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert "refbooks" in response.data
        assert len(response.data["refbooks"]) == 1
        assert response.data["refbooks"][0]["code"] == "MS1"

    def test_get_refbooks_list_with_valid_date(self):
        """Проверка фильтрации по дате (дата позже начала действия версии)"""
        url = f"{reverse('refbook-list')}?date=2022-11-01"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["refbooks"]) == 1

    def test_get_refbooks_list_with_past_date(self):
        """Проверка фильтрации по дате (дата раньше начала действия версии)"""
        url = f"{reverse('refbook-list')}?date=2021-01-01"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["refbooks"]) == 0  # Справочник не должен вернуться

    def test_get_elements_current_version(self):
        """Получение элементов текущей версии (без указания версии)"""
        url = reverse('refbook-elements', kwargs={'pk': self.dict_1.pk})
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert "elements" in response.data
        assert len(response.data["elements"]) == 2
        assert response.data["elements"][0]["code"] == "J00"

    def test_get_elements_specific_version(self):
        """Получение элементов конкретной версии"""
        url = f"{reverse('refbook-elements', kwargs={'pk': self.dict_1.pk})}?version=1.0"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["elements"]) == 2

    def test_check_element_valid(self):
        """Валидация: элемент существует в версии"""
        url = f"{reverse('refbook-check-element', kwargs={'pk': self.dict_1.pk})}?code=J00&value=ОРИ&version=1.0"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["valid"] is True

    def test_check_element_invalid(self):
        """Валидация: элемент с неверным значением"""
        url = f"{reverse('refbook-check-element', kwargs={'pk': self.dict_1.pk})}?code=J00&value=НеправильноеЗначение"
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["valid"] is False
        assert "message" in response.data
