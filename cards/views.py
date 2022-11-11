from django.shortcuts import render, redirect
from .forms import CardForm, CommentForm
from .models import Card, Comment

# Create your views here.


def index(request):
    cards = Card.objects.order_by("-pk")
    context = {"cards": cards}
    return render(request, "cards/index.html", context)


def createindiv(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.socks = request.POST["choice_sock"]
            temp.chimneys = request.POST["choice_chim"]
            # 개인이면 is_indiv에 1
            temp.is_indiv = 1
            temp.save()
            form.save()
            return redirect("cards:index")
    else:
        form = CardForm()
    context = {
        "form": form,
    }

    return render(request, "cards/create_indiv.html", context)


def creategroup(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 그룹이면 is_indiv에 0
            temp.is_indiv = 0
            temp.save()
            form.save()
            return redirect("cards:index")
    else:
        form = CardForm()
    context = {
        "form": form,
    }
    return render(request, "cards/create_group.html", context)


def detail(request, pk):
    cards = Card.objects.get(pk=pk)
    context = {
        "cards": cards,
        "comments": cards.comment_set.all(),
    }

    return render(request, "cards/detail.html", context)


dic = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}


def comment_create(request, pk):
    if request.method == "POST":
        card = Card.objects.get(pk=pk)
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.card = card
            comment.ribbons = request.POST["choice_ribbon"]
            comment.save()
            temp = ""
            for i in str(comment.pk):
                temp += dic[i]
            comment.id_text = temp
            comment.save()
        return redirect("cards:detail", pk)
    else:
        comment_form = CommentForm()
    context = {"comment_form": comment_form}

    return render(request, "cards/comment_create.html", context)
