from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .services import search_places
@require_http_methods(['GET','POST'])
def ask(request):
    q='';places=[];ai_used=False
    if request.method=='POST':
        q=request.POST.get('question','').strip()[:700]
        if q:places,ai_used=search_places(q)
    return render(request,'ai_search/ask.html',{'question':q,'places':places,'ai_used':ai_used})
