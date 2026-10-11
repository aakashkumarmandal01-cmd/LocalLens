from django.test import TestCase
from django.urls import reverse
from locations.models import Country,City
from .models import Category,Place
class PlaceVisibilityTests(TestCase):
    def setUp(self):
        self.country=Country.objects.create(name='India')
        self.city=City.objects.create(country=self.country,name='Jaipur')
        self.category=Category.objects.create(name='Food')
    def test_draft_not_public(self):
        Place.objects.create(name='Draft Place',country=self.country,city=self.city,category=self.category,address='Jaipur')
        response=self.client.get(reverse('place_list'))
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response,'Draft Place')
    def test_published_is_public(self):
        Place.objects.create(name='Published Place',country=self.country,city=self.city,category=self.category,address='Jaipur',status='published')
        response=self.client.get(reverse('place_list'))
        self.assertContains(response,'Published Place')
