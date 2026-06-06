from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .form import SignUpForm
from .models import ProfilUtilisateur, Record


def get_user_role(user):
    if user.is_superuser or user.is_staff:
        return ProfilUtilisateur.ADMIN
    profil, created = ProfilUtilisateur.objects.get_or_create(user=user)
    return profil.role


def redirect_by_role(user):
    role = get_user_role(user)
    if role == ProfilUtilisateur.ADMIN:
        return redirect('dashboard_admin')
    if role == ProfilUtilisateur.ENSEIGNANT:
        return redirect('dashboard_enseignant')
    return redirect('dashboard_etudiant')


def role_required(expected_role):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            role = get_user_role(request.user)
            if role != expected_role:
                messages.success(request, "Vous n'avez pas l'autorisation d'acceder a cette page.")
                return redirect_by_role(request.user)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def home(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    #verification de methode de s'aunthentification
    if request.method=="POST":
       username = request.POST['username']
       password = request.POST['password']
       #verification des donnes username et mode de passe
       user = authenticate(request,username=username,password=password)
       if user is not None:
            login(request, user)
            messages.success(request, "Bien s'authentifier!! ")
            return redirect_by_role(user)
       else:
            messages.success(request,"Erreur authentification...")
            return redirect("home")
    else:
        return render(request, 'home.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Bien se deconnecter ...")
    return redirect('home')

def register_user(request):
    if request.method=="POST":
        f=SignUpForm(request.POST)
        if f.is_valid():
            user = f.save()

            username=f.cleaned_data['username']
            password=f.cleaned_data['password1']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

            messages.success(request, "Bien inscrit!!!")
            return redirect_by_role(user)
        return render(request, 'register.html', {'form':f})
    f=SignUpForm()
    return render(request, 'register.html', {'form':f})


@role_required(ProfilUtilisateur.ADMIN)
def dashboard_admin(request):
    users = ProfilUtilisateur.objects.select_related('user').all()
    return render(request, 'dashboard_admin.html', {'users': users})


@role_required(ProfilUtilisateur.ENSEIGNANT)
def dashboard_enseignant(request):
    return render(request, 'dashboard_enseignant.html')


@role_required(ProfilUtilisateur.ETUDIANT)
def dashboard_etudiant(request):
    return render(request, 'dashboard_etudiant.html')


def customer_record(request, pk):
    if request.user.is_authenticated:
        #voir le record
        cs = get_object_or_404(Record, id=pk)
        return render(request, 'record.html',{'customer_record':cs}) 
    else:
        messages.success(request, "Vous devez etres connecte pour acceder a cette page")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = get_object_or_404(Record, id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully...")
        return redirect('home')
    else:
        messages.success(request, "Vous devez etre connecte")
        return redirect('home')
