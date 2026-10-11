from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg,Count
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from locations.models import Country,City
from .models import Place,Category,SavedPlace
def home(request):
    featured=Place.objects.filter(status='published').select_related('city','country','category').annotate(rating_avg=Avg('reviews__rating',filter=Q(reviews__status='approved')),review_count=Count('reviews',filter=Q(reviews__status='approved'))).order_by('-is_team_verified','-last_verified_at','name')[:6]
    return render(request,'home.html',{'featured':featured,'categories':Category.objects.all()})
def place_list(request):
    qs=Place.objects.filter(status='published').select_related('city','country','category').annotate(rating_avg=Avg('reviews__rating',filter=Q(reviews__status='approved')),review_count=Count('reviews',filter=Q(reviews__status='approved')))
    q=request.GET.get('q','').strip(); country=request.GET.get('country',''); city=request.GET.get('city',''); category=request.GET.get('category',''); budget=request.GET.get('budget',''); rating=request.GET.get('rating',''); sort=request.GET.get('sort','recommended')
    if q:
        for token in q.split()[:8]:
            qs=qs.filter(Q(name__icontains=token)|Q(address__icontains=token)|Q(short_description__icontains=token)|Q(description__icontains=token)|Q(category__name__icontains=token)|Q(city__name__icontains=token))
    if country.isdigit():qs=qs.filter(country_id=country)
    if city.isdigit():qs=qs.filter(city_id=city)
    if category.isdigit():qs=qs.filter(category_id=category)
    if budget.isdigit():qs=qs.filter(Q(price_min__lte=int(budget))|Q(price_min__isnull=True))
    if rating:
        try:qs=qs.filter(rating_avg__gte=float(rating))
        except ValueError:pass
    if sort=='rating':qs=qs.order_by('-rating_avg','name')
    elif sort=='price':qs=qs.order_by('price_min','name')
    elif sort=='recent':qs=qs.order_by('-last_verified_at','name')
    else:qs=qs.order_by('-is_team_verified','-last_verified_at','name')
    return render(request,'places/place_list.html',{'places':qs,'countries':Country.objects.all(),'cities':City.objects.all(),'categories':Category.objects.all(),'filters':request.GET})
def place_detail(request,slug):
    place=get_object_or_404(Place.objects.select_related('city','country','category').prefetch_related('images','amenities'),slug=slug,status='published')
    reviews=place.reviews.filter(status='approved').select_related('user').order_by('-created_at')
    saved=request.user.is_authenticated and SavedPlace.objects.filter(user=request.user,place=place).exists()
    return render(request,'places/place_detail.html',{'place':place,'reviews':reviews,'is_saved':saved})
@login_required
@require_POST
def toggle_saved(request,slug):
    place=get_object_or_404(Place,slug=slug,status='published'); obj,created=SavedPlace.objects.get_or_create(user=request.user,place=place)
    if not created:obj.delete()
    messages.success(request,'Place saved.' if created else 'Place removed from saved places.')
    return redirect('place_detail',slug=slug)
@login_required
def saved_places(request):
    return render(request,'places/saved_places.html',{'places':Place.objects.filter(saved_by__user=request.user,status='published').select_related('city','category')})
