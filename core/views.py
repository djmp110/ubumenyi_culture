from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone

from .models import (
    Pillar, Chapter, Enrollment, Note, Quiz, Question, Choice,
    ForumTopic, ForumReply, LiveSession, Certificate,
)
from .forms import SignUpForm, NoteForm, ForumTopicForm, ForumReplyForm


def home(request):
    featured_chapters = Chapter.objects.filter(is_published=True).order_by('?')[:4]
    upcoming = LiveSession.objects.filter(starts_at__gte=timezone.now())[:3]
    return render(request, 'core/home.html', {
        'featured_chapters': featured_chapters,
        'upcoming_sessions': upcoming,
    })


def about(request):
    return render(request, 'core/about.html')


def pillar_detail(request, slug):
    pillar = get_object_or_404(Pillar, slug=slug)
    chapters = pillar.chapters.filter(is_published=True)
    return render(request, 'core/pillar_detail.html', {
        'pillar': pillar,
        'chapters': chapters,
    })


@login_required
def chapter_detail(request, pillar_slug, chapter_slug):
    chapter = get_object_or_404(
        Chapter, pillar__slug=pillar_slug, slug=chapter_slug, is_published=True
    )

    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, chapter=chapter)
    note, _ = Note.objects.get_or_create(user=request.user, chapter=chapter)

    if request.method == 'POST':
        if 'save_note' in request.POST:
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                messages.success(request, 'Notes saved.')
                return redirect('chapter_detail',
                                pillar_slug=pillar_slug, chapter_slug=chapter_slug)

        if 'mark_complete' in request.POST:
            enrollment.completed = True
            enrollment.progress_percent = 100
            enrollment.save()
            messages.success(request, 'Chapter marked complete.')
            return redirect('chapter_detail',
                            pillar_slug=pillar_slug, chapter_slug=chapter_slug)

    form = NoteForm(instance=note)
    return render(request, 'core/chapter_detail.html', {
        'chapter': chapter,
        'enrollment': enrollment,
        'note_form': form,
        'note': note,
    })


@login_required
def take_quiz(request, pillar_slug, chapter_slug):
    chapter = get_object_or_404(Chapter, pillar__slug=pillar_slug, slug=chapter_slug)
    quiz = get_object_or_404(Quiz, chapter=chapter)

    if request.method == 'POST':
        score = 0
        total = quiz.questions.count()
        for q in quiz.questions.all():
            chosen = request.POST.get(f'q_{q.id}')
            if chosen and q.choices.filter(id=chosen, is_correct=True).exists():
                score += 1
        percent = round((score / total) * 100) if total else 0

        enrollment, _ = Enrollment.objects.get_or_create(user=request.user, chapter=chapter)
        enrollment.quiz_score = percent
        if percent >= quiz.pass_score:
            enrollment.completed = True
            enrollment.progress_percent = 100
            Certificate.objects.get_or_create(user=request.user, chapter=chapter)
        enrollment.save()

        return render(request, 'core/quiz_result.html', {
            'chapter': chapter,
            'score': score,
            'total': total,
            'percent': percent,
            'passed': percent >= quiz.pass_score,
        })

    return render(request, 'core/quiz.html', {'chapter': chapter, 'quiz': quiz})


@login_required
def dashboard(request):
    enrollments = request.user.enrollments.select_related('chapter', 'chapter__pillar')
    certificates = request.user.certificates.select_related('chapter')
    return render(request, 'core/dashboard.html', {
        'enrollments': enrollments,
        'certificates': certificates,
    })


@login_required
def certificate_view(request, certificate_id):
    cert = get_object_or_404(Certificate, certificate_id=certificate_id, user=request.user)
    return render(request, 'core/certificate.html', {'cert': cert})


def forum(request):
    topics = ForumTopic.objects.select_related('author').all()
    return render(request, 'core/forum.html', {'topics': topics})


@login_required
def forum_new(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('forum_topic', pk=topic.pk)
    else:
        form = ForumTopicForm()
    return render(request, 'core/forum_new.html', {'form': form})


def forum_topic(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    replies = topic.replies.select_related('author')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            reply.save()
            return redirect('forum_topic', pk=pk)
    else:
        form = ForumReplyForm()

    return render(request, 'core/forum_topic.html', {
        'topic': topic, 'replies': replies, 'form': form,
    })


def live_sessions(request):
    sessions = LiveSession.objects.all()
    return render(request, 'core/live_sessions.html', {'sessions': sessions})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})