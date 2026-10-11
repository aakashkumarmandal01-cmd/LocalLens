from django.test import TestCase
from django.urls import reverse
from locations.models import Country,City
from places.models import Category,Place
class ReviewTests(TestCase):
    def test_review_requires_login(self):
        country=Country.objects.create(name='India');city=City.objects.create(country=country,name='Jaipur');cat=Category.objects.create(name='Food')
        p=Place.objects.create(name='Cafe',country=country,city=city,category=cat,address='Jaipur',status='published')
        response=self.client.post(reverse('submit_review',args=[p.slug]),{'rating':5,'text':'Good'})
        self.assertEqual(response.status_code,302)
