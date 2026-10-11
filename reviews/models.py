from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from places.models import Place
class Review(models.Model):
    class Status(models.TextChoices):PENDING='pending','Pending'; APPROVED='approved','Approved'; REJECTED='rejected','Rejected'
    place=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='reviews'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='place_reviews')
    rating=models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)]); text=models.TextField(max_length=2000); status=models.CharField(max_length=10,choices=Status.choices,default='pending',db_index=True)
    created_at=models.DateTimeField(auto_now_add=True); moderated_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='moderated_reviews'); moderated_at=models.DateTimeField(null=True,blank=True)
    class Meta:constraints=[models.UniqueConstraint(fields=['place','user'],name='one_review_per_user_place')];ordering=['-created_at']
