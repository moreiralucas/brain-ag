from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import RuralProducer, Crops
from decimal import Decimal

class RuralProducerViewsetTests(APITestCase):

    def setUp(self):
        self.rural_producer = RuralProducer.objects.create(
            document="12345678901",
            producer_name="John Doe",
            farm_name="Doe Farm",
            city="Sample City",
            state="SP",
            total_area=Decimal("100.00"),
            agricultural_area=Decimal("60.00"),
            vegetation_area=Decimal("40.00")
        )
        self.list_url = reverse('ruralproducer-list')
        self.detail_url = reverse('ruralproducer-detail', args=[self.rural_producer.id])
    
    def test_list_rural_producers(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_rural_producer(self):
        data = {
            "document": "77243240003",
            "producer_name": "Jane Doe",
            "farm_name": "Jane Farm",
            "city": "Another City",
            "state": "RJ",
            "total_area": "200.00",
            "agricultural_area": "120.00",
            "vegetation_area": "80.00",
            "crops": [
                {"name": "Corn"},
                {"name": "Wheat"}
            ]
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RuralProducer.objects.count(), 2)
    
    def test_update_rural_producer(self):
        data = {
            "producer_name": "John Updated",
            "farm_name": "Doe Farm Updated"
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.rural_producer.refresh_from_db()
        self.assertEqual(self.rural_producer.producer_name, "John Updated")
    
    def test_delete_rural_producer(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RuralProducer.objects.count(), 0)


class DashboardViewsetTests(APITestCase):

    def setUp(self):
        self.producer1 = RuralProducer.objects.create(
            document="12345678901",
            producer_name="John Doe",
            farm_name="Doe Farm",
            city="Sample City",
            state="SP",
            total_area=Decimal("100.00"),
            agricultural_area=Decimal("60.00"),
            vegetation_area=Decimal("40.00")
        )
        self.producer2 = RuralProducer.objects.create(
            document="23456789012",
            producer_name="Jane Doe",
            farm_name="Jane Farm",
            city="Another City",
            state="RJ",
            total_area=Decimal("200.00"),
            agricultural_area=Decimal("120.00"),
            vegetation_area=Decimal("80.00")
        )
        Crops.objects.create(name="Wheat", producer=self.producer1)
        Crops.objects.create(name="Corn", producer=self.producer2)
        self.url = reverse('dashboard-list')

    def test_dashboard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        
        self.assertEqual(data["total_farms_quantity"], 2)
        
        expected_total_hectares = sum(
            [Decimal("100.00"), Decimal("200.00")]
        )
        self.assertEqual(data["total_farms_hectares"], float(expected_total_hectares))

        per_state = data["per_state"]
        self.assertEqual(len(per_state), 2)
        self.assertIn({"state": "SP", "total_farms": 1}, per_state)
        self.assertIn({"state": "RJ", "total_farms": 1}, per_state)

        per_crop = data["per_crop"]
        self.assertEqual(len(per_crop), 2)
        self.assertIn({"name": "Wheat", "total_per_crop": 1}, per_crop)
        self.assertIn({"name": "Corn", "total_per_crop": 1}, per_crop)

        per_land_use = data["per_land_use"]
        self.assertEqual(per_land_use["total_agricultural_area"], float(Decimal("180.00")))
        self.assertEqual(per_land_use["total_vegetation_area"], float(Decimal("120.00")))
