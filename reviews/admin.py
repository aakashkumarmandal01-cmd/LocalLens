from django.contrib import admin
from django.utils import timezone
from .models import Review
@admin.action(description='Approve selected reviews')
def approve(modeladmin,request,qs):qs.update(status='approved',moderated_by=request.user,moderated_at=timezone.now())
@admin.action(description='Reject selected reviews')
def reject(modeladmin,request,qs):qs.update(status='rejected',moderated_by=request.user,moderated_at=timezone.now())
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=('place','user','rating','status','created_at');list_filter=('status','rating');search_fields=('place__name','user__username','text');actions=[approve,reject]
