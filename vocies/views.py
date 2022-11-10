from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, "vocies.index.html")


def myvocie(request):
    return render(request, "vocies/myvocie.html", {"vocies": request.user.vocies.all()})


def create(request):
    form = VocieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.user = request.user
        temp.save()
        return redirect("vocies:index")
    return render(request, "vocies/create.html", {"form": form})


def detail(request, pk):
    vocie = get_object_or_404(Vocie, pk=pk)
    context = {
        "vocie": vocie,
        "form": CommentForm(),
        "comments": vocie.vocie_comment.all(),
    }
    return render(request, "vocies/detail.html", context)


def comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.vocie = Vocie.objects.get(pk=pk)
        temp.manager = request.user
        temp.save()
        return redirect("vocies:detail", pk)


def manage_page(request):
    return render(request, "vocies/manage_page.html", {"vocies": Vocie.objects.order_by("-pk")})
