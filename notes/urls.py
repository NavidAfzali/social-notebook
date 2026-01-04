from django.urls import path
from .views import *

app_name = 'notes'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('note/<int:note_id>/<slug:note_slug>/',
         NoteDetailsView.as_view(), name='note_details'),
    path('note/delete/<int:note_id>/',
         NoteDeleteView.as_view(), name='note_delete'),
    path('note/update/<int:note_id>/',
         NoteUpdateView.as_view(), name='note_update'),
    path('note/create/', NoteCreateView.as_view(), name='note_create'),
    path('reply/<int:note_id>/<int:comment_id>/',
         NoteReplyView.as_view(), name='note_reply'),
    path('like/<int:note_id>/', NoteLikeView.as_view(), name='note_like'),
]
