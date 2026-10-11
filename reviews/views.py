from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.views.decorators.http import require_POST
from places.models import Place
from .models import Review
from .forms import ReviewForm
@login_required
@require_POST
def submit_review(request,slug):
    p=get_object_or_404(Place,slug=slug,status='published')
    if Review.objects.filter(place=p,user=request.user).exists():
        messages.error(request,'You already reviewed this place.')
        return redirect('place_detail',slug=slug)
    f=ReviewForm(request.POST)
    if f.is_valid():
        r=f.save(commit=False);r.place=p;r.user=request.user;r.status='pending';r.save();messages.success(request,'Review submitted for moderation.')
    else:messages.error(request,'Please enter a valid rating and review.')
    return redirect('place_detail',slug=slug)
