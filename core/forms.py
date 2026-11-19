from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note, ForumTopic, ForumReply


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=120, required=True)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name'].split(' ', 1)
        user.first_name = full_name[0]
        user.last_name = full_name[1] if len(full_name) > 1 else ''
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('body',)
        widgets = {'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your notes…'})}


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ('title', 'body')
        widgets = {'body': forms.Textarea(attrs={'rows': 4})}


class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ('body',)
        widgets = {'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a reply…'})}