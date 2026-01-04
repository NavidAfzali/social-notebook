from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Note, Comment, Like
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NoteCreateUpdateForm, CommentCreateForm, CommentReplyForm, NoteSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    form_class = NoteSearchForm

    def get(self, request):
        notes = Note.objects.all()
        if request.GET.get('search'):
            notes = notes.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'notes': notes, 'form': self.form_class})


class NoteDetailsView(View):
    form_class = CommentCreateForm
    reply_form_class = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.note_instance = get_object_or_404(
            Note, pk=kwargs['note_id'], slug=kwargs['note_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.note_instance.note_comments.filter(is_reply=False)
        return render(request, 'home/note_details.html', {'note': self.note_instance, 'comments': comments, 'form': self.form_class(), 'reply_form': self.reply_form_class})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.note = self.note_instance
            new_comment.save()
            messages.success(
                request, 'Your comment submitted successfully.', 'success')
            return redirect('notes:note_details', self.note_instance.id, self.note_instance.slug)


class NoteDeleteView(LoginRequiredMixin, View):
    def get(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        if note.user.id == request.user.id:
            note.delete()
            messages.error(request, 'Note deleted.', 'success')
        else:
            messages.error(
                request, 'You are not the owner of this note.', 'danger')
        return redirect('notes:home')


class NoteUpdateView(LoginRequiredMixin, View):
    form_class = NoteCreateUpdateForm

    def setup(self, request, *args, **kwargs):
        self.note = get_object_or_404(Note, pk=kwargs['note_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs['note_id'])
        if not note.user.id == request.user.id:
            messages.error(
                request, 'You can just update your notes.', 'warning')
            return redirect('notes:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        note = self.note
        form = self.form_class(instance=note)
        return render(request, 'home/note_update.html', {'form': form, 'note': note})

    def post(self, request, *args, **kwargs):
        note = self.note
        form = self.form_class(request.POST, instance=note)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.slug = slugify(form.cleaned_data['title'])
            tmp.save()
            messages.success(request, 'Note update successfully.', 'success')
            return redirect('notes:note_details', note.id, note.slug)


class NoteCreateView(LoginRequiredMixin, View):
    form_class = NoteCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/note_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.slug = slugify(form.cleaned_data['title'])
            new_note.save()
            messages.success(request, 'Note created successfully', 'success')
            return redirect('notes:note_details', new_note.id, new_note.slug)


class NoteReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, note_id, comment_id):
        note = get_object_or_404(Note, id=note_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.note = note
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'reply added successfully.', 'success')
            return redirect('notes:note_details', note.id, note.slug)


class NoteLikeView(LoginRequiredMixin, View):
    def get(self, request, note_id):
        note = get_object_or_404(Note, id=note_id)
        likes = Like.objects.filter(note=note, user=request.user)
        if likes.exists():
            messages.error(
                request, 'You have already liked this note.', 'info')
        else:
            Like.objects.create(note=note, user=request.user)
            messages.success(request, 'You like this note!', 'success')
        return redirect('notes:note_details', note.id, note.slug)
