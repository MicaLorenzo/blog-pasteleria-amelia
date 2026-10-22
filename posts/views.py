from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def listado_posts(request):
    posts = Post.objects.select_related("autor").all()
    return render(request, "posts/listado_posts.html", {"posts": posts})


def detalle_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/detalle_post.html", {"post": post})


def buscar_posts(request):
    query = request.GET.get("q", "").strip()
    resultados = []
    if query:
        resultados = Post.objects.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)
        )
    return render(
        request, "posts/buscar_posts.html", {"query": query, "resultados": resultados}
    )


@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            messages.success(request, "Post publicado correctamente.")
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm()
    return render(
        request, "posts/post_form.html", {"form": form, "titulo_pagina": "Nuevo post"}
    )


@login_required
def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.autor != request.user:
        return HttpResponseForbidden("No tenés permiso para editar este post: no sos el autor.")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post actualizado correctamente.")
            return redirect("detalle_post", slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(
        request,
        "posts/post_form.html",
        {"form": form, "titulo_pagina": "Editar post", "post": post},
    )


@login_required
def eliminar_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.autor != request.user:
        return HttpResponseForbidden("No tenés permiso para eliminar este post: no sos el autor.")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post eliminado.")
        return redirect("listado_posts")
    return render(request, "posts/post_confirmar_borrado.html", {"post": post})
