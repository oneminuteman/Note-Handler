from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.middleware.csrf import get_token
from django.db import IntegrityError
from .models import Note  # Replaced Task with Note
from .serializers import NoteSerializer, UserSerializer  # Replaced TaskSerializer with NoteSerializer

# --------------------
# AUTHENTICATION APIs
# --------------------

@api_view(['POST'])
def signup(request):
    """ Register a new user """
    data = request.data
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "User registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"error": "Username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_user(request):
    """ User login and return token """
    data = request.data
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """ Logout user and delete token """
    try:
        request.user.auth_token.delete()
    except Exception:
        return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_csrf_token(request):
    """ Return CSRF token for frontend """
    return Response({'csrfToken': get_token(request)})


# --------------------
# NOTE MANAGEMENT APIs (Replaced Tasks with Notes)
# --------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def note_list(request):
    """ Retrieve all notes for the logged-in user """
    notes = Note.objects.filter(user=request.user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def note_create(request):
    """ Create a new note """
    data = request.data
    text = data.get('text')

    if not text:
        return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

    note = Note.objects.create(
        text=text,
        user=request.user
    )
    serializer = NoteSerializer(note)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def note_edit(request, note_id):
    """ Edit a specific note """
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    note.text = request.data.get('text', note.text)
    note.save()
    
    serializer = NoteSerializer(note)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def note_delete(request, note_id):
    """ Delete a specific note """
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
