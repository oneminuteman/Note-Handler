from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import signup, login_user , logout_user  # Import signup and login views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include all user authentication and task-related URLs
    path('api/', include('users.urls')),  
    
    # DRF Auth Token (for login authentication)
    path('api/token/', obtain_auth_token, name='api_token_auth'),

    # Signup and Login endpoints
    path('api/signup/', signup, name='signup'),
    path('api/login/', login_user, name='login'),
    path("api/logout/", logout_user, name="logout"),
    path('api/notes/', include('notes.urls')),  

]

