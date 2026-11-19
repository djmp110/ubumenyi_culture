
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Pillar(models.Model):
    """Top-level learning category: Language, History, Arts, Heritage."""
    name = models.CharField(max_length=80)
    name_kinyarwanda = models.CharField(max_length=80, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=20, default='🌿',
                            help_text='Emoji icon shown on the card')
    color = models.CharField(max_length=7, default='#1d6e5c',
                             help_text='Hex color for the card accent')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    """A lesson inside a Pillar. Can be video, book, audio, or article."""
    TYPE_CHOICES = [
        ('video', 'Video Lesson'),
        ('book', 'Digital Book'),
        ('audio', 'Audio Recording'),
        ('article', 'Written Article'),
    ]
    pillar = models.ForeignKey(Pillar, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    title_kinyarwanda = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(blank=True)
    summary = models.TextField(blank=True)
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='video')
    video_url = models.URLField(blank=True)
    book_file = models.FileField(upload_to='books/', blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    body = models.TextField(blank=True, help_text='For articles; Markdown-ish text')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    duration_minutes = models.PositiveSmallIntegerField(default=10)
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pillar', 'order', 'title']
        unique_together = ('pillar', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:60] or str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pillar.name} · {self.title}'


class Quiz(models.Model):
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE, related_name='quiz')
    pass_score = models.PositiveSmallIntegerField(default=70, help_text='Percentage required')

    def __str__(self):
        return f'Quiz for {self.chapter.title}'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=300)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Enrollment(models.Model):
    """A user's progress through a chapter."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='enrollments')
    started_at = models.DateTimeField(auto_now_add=True)
    last_position = models.CharField(max_length=200, blank=True,
                                     help_text='Video timestamp or page number')
    progress_percent = models.PositiveSmallIntegerField(default=0)
    completed = models.BooleanField(default=False)
    quiz_score = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f'{self.user.username} · {self.chapter.title}'


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='notes')
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f'Note by {self.user.username} on {self.chapter.title}'


class ForumTopic(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class ForumReply(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Reply to {self.topic.title} by {self.author.username}'


class LiveSession(models.Model):
    title = models.CharField(max_length=200)
    host = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=60)
    join_url = models.URLField(blank=True)

    class Meta:
        ordering = ['starts_at']

    def __str__(self):
        return f'{self.title} ({self.starts_at:%Y-%m-%d %H:%M})'


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f'{self.user.username} · {self.chapter.title}'