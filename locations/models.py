from django.db import models
from django.utils.text import slugify
class Country(models.Model):
    name=models.CharField(max_length=100,unique=True); code=models.CharField(max_length=3,blank=True); slug=models.SlugField(unique=True,blank=True)
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.name)
        super().save(*a,**kw)
    def __str__(self):return self.name
class City(models.Model):
    country=models.ForeignKey(Country,on_delete=models.PROTECT,related_name='cities'); name=models.CharField(max_length=120); slug=models.SlugField(blank=True)
    class Meta: unique_together=('country','name')
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.name)
        super().save(*a,**kw)
    def __str__(self):return f'{self.name}, {self.country.name}'
class Neighborhood(models.Model):
    city=models.ForeignKey(City,on_delete=models.CASCADE,related_name='neighborhoods'); name=models.CharField(max_length=120)
    class Meta: unique_together=('city','name')
    def __str__(self):return f'{self.name} ({self.city.name})'
