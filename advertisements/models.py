from django.db import models
from django.utils import timezone
class Advertisement(models.Model):
    title=models.CharField(max_length=140);image=models.ImageField(upload_to='ads/%Y/%m/',blank=True);destination_url=models.URLField(blank=True);active=models.BooleanField(default=False);starts_at=models.DateTimeField(null=True,blank=True);ends_at=models.DateTimeField(null=True,blank=True)
    def is_live(self):
        n=timezone.now();return self.active and (not self.starts_at or self.starts_at<=n) and (not self.ends_at or self.ends_at>=n)
    def __str__(self):return self.title
