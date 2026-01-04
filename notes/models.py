from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Note(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=60)
    body = models.TextField()
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'slug'],
                name='unique_note_slug_per_user'
            )
        ]

    def __str__(self):
        return f'{self.slug} / {self.updated}'

    def get_absolute_url(self):
        return reverse("notes:note_details", args=(self.pk, self.slug))

    def likes_count(self):
        return self.note_like.count()


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_comments')
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name='note_comments')
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.body[:15]}'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_like')
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name='note_like')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'note'],
                name='unique_like_per_user_note'
            )
        ]

    def __str__(self):
        return f'{self.user.username} likes {self.note.title}'
