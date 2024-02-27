from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from djokalante.LoginBackend import LoginBackend


def page_de_connexion(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'commons/header.html')


def se_connecter(request):
    if request.method != "POST":
        return HttpResponse("<h2>Methode non autorisee</h2>")
    else:
        user = LoginBackend.authenticate(request, username=request.POST.get("username"),
                                         password=request.POST.get("password"))
        print(f"{user}")
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Informations d'identification invalides")
            return HttpResponseRedirect("/")


def se_deconnecter(request):
    logout(request)
    return HttpResponseRedirect("/")
