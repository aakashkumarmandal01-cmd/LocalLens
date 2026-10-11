import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Category,Amenity,Place,PlaceImage,SavedPlace
class PlaceImageInline(admin.TabularInline): model=PlaceImage; extra=1
@admin.action(description='Export selected places to CSV')
def export_csv(modeladmin,request,queryset):
    r=HttpResponse(content_type='text/csv'); r['Content-Disposition']='attachment; filename="locallens_places.csv"'; w=csv.writer(r); w.writerow(['name','category','country','city','address','status','verified','last_verified_at'])
    for p in queryset:w.writerow([p.name,p.category.name,p.country.name,p.city.name,p.address,p.status,p.is_team_verified,p.last_verified_at])
    return r
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display=('name','category','city','status','is_team_verified','last_verified_at','updated_at'); list_filter=('status','category','country','city','is_team_verified'); search_fields=('name','address','description','city__name'); inlines=[PlaceImageInline]; actions=[export_csv]; readonly_fields=('created_at','updated_at')
    fieldsets=(('Listing',{'fields':('name','slug','category','status','short_description','description')}),('Location',{'fields':('country','city','neighborhood','address','latitude','longitude')}),('Details',{'fields':('price_min','price_max','currency','opening_hours','phone','website','amenities','dietary_options','accessibility_info')}),('Media',{'fields':('cover_image','panorama_url','model_3d_url')}),('Verification',{'fields':('is_team_verified','last_verified_at','next_review_date','internal_notes')}),('Audit',{'fields':('created_by','updated_by','created_at','updated_at')}))
admin.site.register(Category); admin.site.register(Amenity); admin.site.register(PlaceImage); admin.site.register(SavedPlace)
