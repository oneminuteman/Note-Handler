from django.urls import path
from .views import signup, login_user, logout_user, note_list, note_create, note_edit, note_delete, get_csrf_token  

urlpatterns = [
    # Authentication Endpoints
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
    
    # Task Management Endpoints
    path('api/notes/', note_list, name='note-list'),
    path('api/notes/create/', note_create, name='note-create'),
    path('api/notes/<int:note_id>/edit/', note_edit, name='note-edit'),
    path('api/notes/<int:note_id>/delete/', note_delete, name='note-delete'),
]


