from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def signup(request):
    gender = request.POST.get("gender")
    age = request.POST.get("age")
    print(gender, age)
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            forms = form.save(commit=False)
            forms.gender = gender
            forms.age = age
            forms.save()
            return redirect("accounts:index")
    else:
        form = SignupForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def index(request):
    return render(request, "accounts/index.html")


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("accounts:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)
