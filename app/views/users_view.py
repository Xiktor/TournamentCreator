from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

from app.decorators import allowed_users
from app.forms.users_form import CreateUserForm


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='user')
                user.groups.add(group)
                messages.success(request, 'Konto ' + username + ' zarejestrowane pomyślnie' )

                return redirect('login')
            else:
                messages.error(request, form.errors)
        context = {'form': form}
        return render(request, 'app/register.html', context)


@allowed_users(allowed_roles=['admin'])
def create_admin(request):
    if request.user.is_superuser:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get('username')
                user.is_superuser = True
                user.is_staff = True
                user.save()
                group = Group.objects.get(name='admin')
                user.groups.add(group)
                messages.success(request, 'Administrator ' + username + ' zarejestrowany pomyślnie')

                return redirect('create_admin')
            else:
                messages.error(request, form.errors)
        context = {'form': form}
        return render(request, 'app/create_admin.html', context)
    else:
        messages.error(request, 'Nie jesteś administratorem')
        return redirect(home)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Niepoprawna nazwa użytkownika lub hasło.')
        context = {}
        return render(request, 'app/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'app/home.html')
