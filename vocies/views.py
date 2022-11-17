from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, "vocies/index.html")


@login_required
def myvocie(request):
    return render(request, "vocies/myvocie.html", {"vocies": request.user.vocies.all()})


@login_required
def create(request):
    form = VocieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.user = request.user
        temp.save()
        return redirect("vocies:index")
    return render(request, "vocies/create.html", {"form": form})


@login_required
def detail(request, pk):
    vocie = get_object_or_404(Vocie, pk=pk)
    if request.user == vocie.user or request.user.is_superuser:
        context = {
            "vocie": vocie,
            "form": CommentForm(),
            "comments": vocie.vocie_comment.all(),
        }
        return render(request, "vocies/detail.html", context)
    messages.warning(request, "작성자만 접근할 수 있습니다.")
    return redirect("vocies:index")

@login_required
def update(request, pk):
    vocie = get_object_or_404(Vocie, pk=pk)
    if request.user == vocie.user:
        if request.method == 'POST':
            form = VocieForm(request.POST, request.FILES, instance=vocie)
            if form.is_valid():
                form.save()
                return redirect("vocies:detail", vocie.pk)
        else:
            form = VocieForm(instance=vocie)
        return render(request, "vocies/update.html", {"form": form})
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("vocies:detail", pk)


@login_required
def comment(request, pk):
    if request.user.is_superuser:
        form = CommentForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.vocie = Vocie.objects.get(pk=pk)
            temp.manager = request.user
            temp.save()
            return redirect("vocies:detail", pk)
    messages.warning(request, "관리자만 접근할 수 있습니다.")
    return redirect("vocies:index")


def delete_comment(request, pk, super_pk):
    if request.user.is_superuser:
        comment_delete = Comment.objects.get(pk=pk)
        comment_delete.delete()
    return redirect("vocies:detail", super_pk)


# @permission_required('vocies.index', raise_exception=True)
def manage_page(request):
    return render(request, "vocies/manage_page.html", {"vocies": Vocie.objects.order_by("-pk")})
