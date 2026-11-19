from .models import Pillar

def site_context(request):
    return {
        'pillars': Pillar.objects.all(),
        'site_name': 'Ubumenyi Hub',
        'site_tagline': 'Learn Rwanda’s Culture — Language, History, Arts, Heritage',
    }