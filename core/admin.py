from django.contrib import admin
from .models import (
    Pillar, Chapter, Quiz, Question, Choice,
    Enrollment, Note, ForumTopic, ForumReply,
    LiveSession, Certificate,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2
    show_change_link = True


@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_kinyarwanda', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'pillar', 'content_type', 'is_published', 'order')
    list_filter = ('pillar', 'content_type', 'is_published')
    search_fields = ('title', 'title_kinyarwanda', 'summary')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    inlines = [ChoiceInline]


admin.site.register(Quiz)
admin.site.register(Enrollment)
admin.site.register(Note)
admin.site.register(ForumTopic)
admin.site.register(ForumReply)
admin.site.register(LiveSession)
admin.site.register(Certificate)

admin.site.site_header = 'Ubumenyi Hub — Culture Admin'
admin.site.site_title = 'Ubumenyi Hub Admin'
admin.site.index_title = 'Manage Rwandan culture content'