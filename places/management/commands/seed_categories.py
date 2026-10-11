from django.core.management.base import BaseCommand
from locations.models import Country,City
from places.models import Category
class Command(BaseCommand):
    help='Create starter country, Jaipur city and categories'
    def handle(self,*args,**kwargs):
        country,_=Country.objects.get_or_create(name='India',defaults={'code':'IN'})
        City.objects.get_or_create(country=country,name='Jaipur')
        for name in ['Food & Drink','Hotels & Stays','Attractions','Healthcare','Transport','Groceries & Shopping','Banks & ATMs','Repairs & Services','Housing','Work & Study','Community & Events','Family & Accessibility']:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Starter location and categories created.'))
