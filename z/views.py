from uuid import UUID
from random import choice as rd_choice
from dataclasses import dataclass

from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import transaction, DatabaseError
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Treasure, Token, Photo


# Create your views here.
@dataclass
class Error:
    code: int
    name: str
    message: str

    def render(self, request):
        return render(request, 'z/error.html', {"error": self}, status=self.code)

def create_treasure(data: dict, files: MultiValueDict):
    if 'lon' in data and 'lat' in data:
        point = Point(float(data['lon']), float(data['lat']))
    else:
        raise ValueError()
    
    if 'desc' in data:
        desc = data['desc']
    else:
        raise ValueError()
    
    if 'photo' in files:
        photos = files.getlist('photo')
    else:
        raise ValueError()

    treasure = Treasure(location=point, description=desc)
    photos = map(lambda file: Photo(file=file, treasure=treasure), photos)
    return treasure, photos


def index(request: HttpRequest):
    return render(request, 'z/index.html')

def post_treasure(request: HttpRequest):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        try:
            treasure, photos = create_treasure(request.POST, request.FILES)
        except ValueError as e:
            errors = None # TODO
            return render(request, 'z/post.html', {'errors': errors})
        try:
            with transaction.atomic():
                treasure.full_clean()
                treasure.save()
                for photo in photos:
                    photo.full_clean()
                    photo.save()
                new_token = Token(user=user)
                new_token.full_clean()
                new_token.save()
        except ValidationError as e:
            print(e)
            errors = None # TODO
            return render(request, 'z/post.html', {'errors': errors})
        except DatabaseError:
            return Error(507, "Insufficient Storage", "Could not commit transaction").render(request)
        
        return HttpResponseRedirect(reverse('get_token', kwargs={'pk': new_token.id}))

    else:
        return render(request, 'z/post.html', {'errors': None})


def get_treasure(request: HttpRequest, pk: UUID):
    try:
        treasure = get_object_or_404(Treasure, pk=pk)
    except Http404:
        return Error(404, "Not Found", "Treasure with such id is not found").render(request)

    return render(request, 'z/get.html', {'treasure': treasure})

def get_new_treasure(request: HttpRequest):
    user = request.user if request.user.is_authenticated else None
    if 'token' not in request.GET:
        return render(request, 'z/get_new.html')
    pk = request.GET.get('token')
    try:
        token = Token.objects.get(pk=pk)
    except Token.DoesNotExist:
        return Error(404, 'Not Found', 'Such token does not exist').render(request)
    except ValidationError as e:
        return Error(400, 'Bad Request', "<br>".join(e)).render(request)
    if token.protected and token.user != request.user:
        return Error(403, 'Forbidden', "This token protected by its owner").render(request)
    if not token.active:
        return HttpResponseRedirect(reverse('get_token', kwargs={'pk': token.id}))
    
    try:
        treasure = rd_choice(Treasure.objects.filter(status=Treasure.Status.POSTED))
    except IndexError:
        return Error(500, "Iternal Server Error", "There are no valid treasures").render(request)

    try:
        with transaction.atomic():
            token.active = False
            treasure.status = Treasure.Status.RECEIVED
            treasure.user = user
            token.save()
            treasure.save()
    except DatabaseError:
        return Error(507, "Insufficient Storage", "Could not commit transaction").render(request)
    
    return HttpResponseRedirect(reverse('get_treasure', kwargs={'pk': treasure.pk}))
    

def get_token(request: HttpRequest, pk: UUID):
    try:
        token = get_object_or_404(Token, id=pk)
    except Http404:
        return Error(404, 'Not Found', 'Such token does not exist').render(request)
    if token.protected and token.user != request.user:
        return Error(403, 'Forbidden', "This token protected by its owner").render(request)
    page = render(request, 'z/token.html', {'token': token})
    if token.new:
        token.new = False
        token.save()
    
    return page

def register_user(request: HttpRequest):
    if request.method == 'POST':
        errors = {}
        username = request.POST.get('username')
        if not username:
            errors['username'] = ['Username is required']

        password = request.POST.get('password')
        if not password:
            errors['password'] = ['Password is required']

        if errors:
            return render(request, 'z/registration.html', {'errors': errors})
        
        user = User.objects.create_user(username=username, password=password)

        login(request, user)

        return redirect('index')

    return render(request, 'z/registration.html')

def login_user(request: HttpRequest):
    if request.method == 'POST':
        errors = {}
        username = request.POST.get('username')
        if not username:
            errors['username'] = ['Username is required']

        password = request.POST.get('password')
        if not password:
            errors['password'] = ['Password is required']

        if errors:
            print(errors)
            return render(request, 'z/login.html', {'errors': errors})
        
        user = authenticate(username=username, password=password)

        if not user:
            errors['main'] = ['This user does not exist']
            print(errors)
            return render(request, 'z/login.html', {'errors': errors})
        
        next = request.GET.get('next', 'index')
        login(request, user)
        return redirect(next)

    return render(request, 'z/login.html')

def logout_user(request: HttpRequest):

    logout(request)
    next = request.GET.get('next', 'index')
    return redirect(next)

@login_required(redirect_field_name='next')
def my_tokens(request: HttpRequest):
    tokens = request.user.token_set.all()

    return render(request, 'z/my_tokens.html', {'tokens': tokens})

@login_required(redirect_field_name='next')
def assign_token(request: HttpRequest):
    pk = request.GET.get('token')
    try:
        token = get_object_or_404(Token, id=pk)
    except Http404:
        return Error(404, 'Not Found', 'Such token does not exist').render(request)
    
    if token.user == request.user:
        return Error(400, 'Bad request', 'This token is already yours').render(request)
    
    if token.user is not None:
        return Error(403, 'Forbidden', 'This token belongs to another user').render(request)
    
    token.user = request.user
    token.save()

    return redirect('my_tokens')

@login_required(redirect_field_name='next')
def protect_token(request: HttpRequest):
    pk = request.GET.get('pk')
    try:
        token = get_object_or_404(Token, id=pk)
    except Http404:
        return Error(404, 'Not Found', 'Such token does not exist').render(request)
    
    if token.user != request.user:
        return Error(403, 'Forbidden', 'This token is not yours').render(request)
    
    unprotect = request.GET.get('unprotect', False)
    next = request.GET.get('next', 'my_tokens')

    token.protected = not bool(unprotect)
    token.save()

    return redirect(next)

@login_required(redirect_field_name='next')
def my_treasures(request: HttpRequest):
    treasures = request.user.treasure_set.all()

    return render(request, 'z/my_treasures.html', {"treasures": treasures})

@login_required(redirect_field_name='next')
def assign_treasure(request: HttpRequest):
    pk = request.GET.get('id')
    try:
        treasure = get_object_or_404(Token, id=pk)
    except Http404:
        return Error(404, 'Not Found', 'Such treasure does not exist').render(request)
    
    if treasure.user == request.user:
        return Error(400, 'Bad request', 'This treasure is already yours').render(request)
    
    if treasure.user is not None:
        return Error(403, 'Forbidden', 'This treasure belongs to another user').render(request)
    
    treasure.user = request.user
    treasure.save()

    return redirect('my_treasures')