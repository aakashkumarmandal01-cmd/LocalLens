from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from locations.models import Country,City,Neighborhood
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True); slug=models.SlugField(unique=True,blank=True); icon=models.CharField(max_length=40,blank=True)
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.name)
        super().save(*a,**kw)
    def __str__(self):return self.name
class Amenity(models.Model):
    name=models.CharField(max_length=80,unique=True)
    def __str__(self):return self.name
class Place(models.Model):
    class Status(models.TextChoices): DRAFT='draft','Draft'; PUBLISHED='published','Published'; HIDDEN='hidden','Hidden'; ARCHIVED='archived','Archived'
    name=models.CharField(max_length=180); slug=models.SlugField(max_length=200,unique=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='places'); country=models.ForeignKey(Country,on_delete=models.PROTECT,related_name='places'); city=models.ForeignKey(City,on_delete=models.PROTECT,related_name='places'); neighborhood=models.ForeignKey(Neighborhood,on_delete=models.SET_NULL,null=True,blank=True,related_name='places')
    address=models.TextField(); latitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True); longitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    short_description=models.CharField(max_length=260,blank=True); description=models.TextField(blank=True); price_min=models.PositiveIntegerField(null=True,blank=True); price_max=models.PositiveIntegerField(null=True,blank=True); currency=models.CharField(max_length=8,default='INR')
    opening_hours=models.TextField(blank=True); phone=models.CharField(max_length=40,blank=True); website=models.URLField(blank=True); amenities=models.ManyToManyField(Amenity,blank=True)
    dietary_options=models.CharField(max_length=240,blank=True); accessibility_info=models.TextField(blank=True); cover_image=models.ImageField(upload_to='places/covers/%Y/%m/',blank=True)
    panorama_url=models.URLField(blank=True); model_3d_url=models.URLField(blank=True); status=models.CharField(max_length=12,choices=Status.choices,default=Status.DRAFT,db_index=True)
    is_team_verified=models.BooleanField(default=False); last_verified_at=models.DateField(null=True,blank=True); next_review_date=models.DateField(null=True,blank=True); internal_notes=models.TextField(blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='created_places'); updated_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='updated_places')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['name']; indexes=[models.Index(fields=['city','category','status'])]
    def save(self,*a,**kw):
        if not self.slug:
            base=slugify(self.name)[:170] or 'place'; candidate=base; n=2
            while Place.objects.filter(slug=candidate).exclude(pk=self.pk).exists(): candidate=f'{base}-{n}'; n+=1
            self.slug=candidate
        super().save(*a,**kw)
    @property
    def average_rating(self):
        from django.db.models import Avg
        return self.reviews.filter(status='approved').aggregate(v=Avg('rating'))['v']
    def maps_url(self):
        from urllib.parse import quote
        dest=f'{self.latitude},{self.longitude}' if self.latitude is not None and self.longitude is not None else self.address
        return 'https://www.google.com/maps/dir/?api=1&destination='+quote(dest)
    def rapido_url(self):return 'https://www.rapido.bike/'
    def get_absolute_url(self):return reverse('place_detail',kwargs={'slug':self.slug})
    def __str__(self):return self.name
class PlaceImage(models.Model):
    place=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='images'); image=models.ImageField(upload_to='places/gallery/%Y/%m/'); alt_text=models.CharField(max_length=180,blank=True); sort_order=models.PositiveIntegerField(default=0); uploaded_at=models.DateTimeField(auto_now_add=True)
    class Meta:ordering=['sort_order','id']
class SavedPlace(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='saved_places'); place=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='saved_by'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta:constraints=[models.UniqueConstraint(fields=['user','place'],name='unique_saved_place')]
