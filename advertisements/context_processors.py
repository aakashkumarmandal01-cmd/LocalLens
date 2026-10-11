from .models import Advertisement
def active_ad(request):
    try:ad=next((x for x in Advertisement.objects.all() if x.is_live()),None)
    except Exception:ad=None
    return {'active_ad':ad}
