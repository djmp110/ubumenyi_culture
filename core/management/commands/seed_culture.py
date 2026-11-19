from django.core.management.base import BaseCommand
from core.models import Pillar, Chapter


PILLARS = [
    {
        'name': 'Language', 'name_kinyarwanda': 'Ururimi', 'icon': '🗣️', 'color': '#1d6e5c',
        'description': 'Kinyarwanda reading, writing, proverbs (imigani), and everyday expressions.',
        'chapters': [
            {'title': 'Kinyarwanda Greetings', 'title_kinyarwanda': 'Indamukanyo',
             'summary': 'How to greet people at different times of day and with different levels of respect.',
             'content_type': 'video', 'video_url': 'https://www.youtube.com/embed/xxx', 'duration_minutes': 8},
            {'title': 'Rwandan Proverbs', 'title_kinyarwanda': 'Imigani',
             'summary': 'Ten foundational proverbs and what they teach about Rwandan values.',
             'content_type': 'article', 'duration_minutes': 12},
        ]
    },
    {
        'name': 'History', 'name_kinyarwanda': 'Amateka', 'icon': '📜', 'color': '#8b4513',
        'description': 'From the Kingdom of Rwanda to today — the full arc of a proud nation.',
        'chapters': [
            {'title': 'Pre-Colonial Kingdoms', 'title_kinyarwanda': 'Ubwami bwa mbere',
             'summary': 'The structure of the Rwandan monarchy and its regional influence.',
             'content_type': 'article', 'duration_minutes': 15},
        ]
    },
    {
        'name': 'Arts & Music', 'name_kinyarwanda': 'Ubuhanzi n’Umuziki', 'icon': '🥁', 'color': '#c76a1e',
        'description': 'Intore dance, ingoma drumming, crafts, and poetry.',
        'chapters': [
            {'title': 'The Intore Dance', 'title_kinyarwanda': 'Intore',
             'summary': 'Origins, movements, and meaning of Rwanda’s iconic dance.',
             'content_type': 'video', 'duration_minutes': 14},
        ]
    },
    {
        'name': 'Heritage', 'name_kinyarwanda': 'Umurage', 'icon': '🌿', 'color': '#2c7a4d',
        'description': 'Sacred sites, traditional food, ceremonies, and the environment.',
        'chapters': [
            {'title': 'Traditional Rwandan Food', 'title_kinyarwanda': 'Ibiryo gakondo',
             'summary': 'From ubugali to isombe — the dishes that tell our story.',
             'content_type': 'article', 'duration_minutes': 10},
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed culture pillars and sample chapters'

    def handle(self, *args, **kwargs):
        for order, p in enumerate(PILLARS):
            chapters = p.pop('chapters')
            pillar, created = Pillar.objects.get_or_create(
                name=p['name'], defaults={**p, 'order': order}
            )
            for i, c in enumerate(chapters):
                Chapter.objects.get_or_create(
                    pillar=pillar, title=c['title'],
                    defaults={**c, 'order': i, 'is_published': True}
                )
            self.stdout.write(f'Pillar: {pillar.name} {"(created)" if created else "(exists)"}')
        self.stdout.write(self.style.SUCCESS('Culture content seeded!'))