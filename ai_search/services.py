import json,os
from django.db.models import Q,Avg,Count
from places.models import Place
def search_places(question):
    filters={};ai_used=False;api_key=os.getenv('OPENAI_API_KEY','').strip()
    if api_key:
        try:
            from openai import OpenAI
            client=OpenAI(api_key=api_key,timeout=8,max_retries=1)
            result=client.chat.completions.create(model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),temperature=0,response_format={'type':'json_object'},messages=[
                {'role':'system','content':'Return JSON only with keywords (string), category (string), city (string), max_price (integer or null). Extract filters only. Never name or invent businesses.'},
                {'role':'user','content':question[:700]}])
            filters=json.loads(result.choices[0].message.content or '{}');ai_used=True
        except Exception:filters={}
    qs=Place.objects.filter(status='published').select_related('city','country','category').annotate(rating_avg=Avg('reviews__rating',filter=Q(reviews__status='approved')),review_count=Count('reviews',filter=Q(reviews__status='approved')))
    keywords=str(filters.get('keywords') or question)[:160]
    for token in [x for x in keywords.split() if len(x)>2][:8]:
        qs=qs.filter(Q(name__icontains=token)|Q(short_description__icontains=token)|Q(description__icontains=token)|Q(category__name__icontains=token)|Q(city__name__icontains=token)|Q(neighborhood__name__icontains=token)|Q(amenities__name__icontains=token))
    if filters.get('category'):qs=qs.filter(category__name__icontains=str(filters['category'])[:80])
    if filters.get('city'):qs=qs.filter(city__name__icontains=str(filters['city'])[:80])
    price=filters.get('max_price')
    if isinstance(price,int) and price>=0:qs=qs.filter(Q(price_min__lte=price)|Q(price_min__isnull=True))
    return qs.distinct().order_by('-is_team_verified','-rating_avg','-last_verified_at','name')[:12],ai_used
