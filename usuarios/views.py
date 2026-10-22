from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PerfilUsuarioForm, RegistroForm
from .models import PerfilUsuario


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(user=user)
            messages.success(request, "Cuenta creada. Ya podés iniciar sesión.")
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})


@login_required
def perfil(request):
    perfil_usuario, _creado = PerfilUsuario.objects.get_or_create(user=request.user)
    return render(request, "usuarios/perfil.html", {"perfil": perfil_usuario})


@login_required
def editar_perfil(request):
    perfil_usuario, _creado = PerfilUsuario.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("perfil")
    else:
        form = PerfilUsuarioForm(instance=perfil_usuario)
    return render(request, "usuarios/editar_perfil.html", {"form": form})
