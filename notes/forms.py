from django import forms
from .models import Note, Comment


class NoteCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'body', 'is_public')


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'add comment for this note.'}),
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'reply to this comment'}),
        }


class NoteSearchForm(forms.Form):
    search = forms.CharField()
