from datetime import date
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from places.models import Place
from reviews.models import Review
@user_passes_test(lambda u:u.is_authenticated and u.is_staff)
def index(request):
    return render(request,'dashboard/index.html',{'places_total':Place.objects.count(),'published_total':Place.objects.filter(status='published').count(),'pending_reviews':Review.objects.filter(status='pending').count(),'outdated_total':Place.objects.filter(next_review_date__lt=date.today()).count(),'recent_places':Place.objects.order_by('-updated_at')[:8]})
