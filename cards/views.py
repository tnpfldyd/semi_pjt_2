from django.shortcuts import render, redirect


from .forms import *
from .models import *


import requests, os, json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here.


@login_required
def index(request):
    cards = UserCard.objects.order_by("-pk")
    groupcards = Groupcard.objects.order_by("-pk")
    user = get_user_model().objects.get(pk=request.user.pk)
    context = {"cards": cards, "groupcards": groupcards, "user": user}
    return render(request, "cards/index.html", context)


# 개인카드 생성, 수정, 삭제, 디테일


@login_required
def create_indiv(request):
    if request.method == "POST":
        form = UserCardForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.socks = request.POST["choice_sock"]
            temp.chimneys = request.POST["choice_chim"]
            temp.save()
            return redirect("cards:index")
    else:
        form = UserCardForm()
    context = {
        "form": form,
    }
    return render(request, "cards/create_indiv.html", context)


def indiv_detail(request):
    cards = UserCard.objects.get(user=request.user.pk)
    context = {
        "cards": cards,
        "comments": cards.usercomment_set.all(),
    }
    return render(request, "cards/indiv_detail.html", context)


def usercard_update(request, pk):
    cards = UserCard.objects.get(user_id=pk)
    if request.method == "POST":
        form = UserCardForm(request.POST, instance=cards)
        if form.is_valid():
            if form.is_valid():
                temp = form.save(commit=False)
                temp.user = request.user
                # 라디오 버튼 'name'='id'로 들어옴
                # name==choice, id=1,2,3으로 설정
                temp.socks = request.POST["choice_sock"]
                temp.chimneys = request.POST["choice_chim"]
                temp.save()
                return redirect("cards:indiv_detail")
    else:
        form = UserCardForm(instance=cards)
    context = {"form": form}
    return render(request, "cards/usercard_update.html", context=context)


def usercard_delete(request):
    card = UserCard.objects.get(user_id=request.user.pk)
    card.delete()
    return redirect("cards:index")


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


def usercard_comment(request, pk):
    if request.method == "POST":
        card = UserCard.objects.get(pk=pk)
        comment_form = UserCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.usercard = card
            comment.ribbons = request.POST["choice_ribbon"]
            comment.save()
            temp = ""
            for i in str(comment.pk):
                temp += dic[i]
            comment.id_text = temp
            comment.save()
            url = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type": "refresh_token",
                "client_id": os.getenv("KAKAO_ID"),
                "refresh_token": card.user.refresh_token,
                "client_secret": os.getenv("KAKAO_SECRET"),
            }
            response = requests.post(url, data=data).json()
            url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
            access_token = response["access_token"]
            headers = {"Authorization": "Bearer " + access_token}
            data = {
                "template_object": json.dumps(
                    {
                        "object_type": "text",
                        "text": request.user.nickname + "님이 트리에 글을 남겨주셨어요.",
                        "link": {"web_url": "http://localhost:8000/cards/" + str(pk)},
                    }
                )
            }
            response = requests.post(url, headers=headers, data=data)
            return redirect("cards:indiv_detail")
    else:
        comment_form = UserCommentForm()
    context = {"comment_form": comment_form}

    return render(request, "cards/usercard_comment.html", context)


# 그룹카드 생성, 수정, 삭제, 디테일


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupCardForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.socks = request.POST["choice_sock"]
            temp.chimneys = request.POST["choice_chim"]
            temp.save()
            return redirect("cards:index")
    else:
        form = GroupCardForm()
    context = {
        "form": form,
    }

    return render(request, "cards/create_group.html", context)


def group_detail(request, pk):
    groupcards = Groupcard.objects.get(pk=pk)
    context = {
        "groupcards": groupcards,
        "comments": groupcards.groupcomment_set.all(),
    }

    return render(request, "cards/group_detail.html", context)


def card_update(request, pk):

    cards = Groupcard.objects.get(user_id=request.user.pk, is_indiv=1)

    if request.method == "POST":
        form = GroupCardForm(request.POST, instance=cards)
        if form.is_valid():
            if form.is_valid():
                temp = form.save(commit=False)
                temp.user = request.user
                # 라디오 버튼 'name'='id'로 들어옴
                # name==choice, id=1,2,3으로 설정
                temp.socks = request.POST["choice_sock"]
                temp.chimneys = request.POST["choice_chim"]
                temp.save()
                return redirect("cards:indiv_detail")
    else:
        form = GroupCardForm(instance=cards)
    context = {"form": form}
    return render(request, "cards/card_update.html", context=context)



def groupcard_update(request, pk):
    cards = Groupcard.objects.get(pk=pk)
    if request.method == "POST":
        form = GroupCardForm(request.POST, instance=cards)
        if form.is_valid():
            if form.is_valid():
                temp = form.save(commit=False)
                temp.user = request.user
                # 라디오 버튼 'name'='id'로 들어옴
                # name==choice, id=1,2,3으로 설정
                temp.socks = request.POST["choice_sock"]
                temp.chimneys = request.POST["choice_chim"]
                temp.save()
                return redirect("cards:group_detail", cards.pk)
    else:
        form = GroupCardForm(instance=cards)
    context = {"form": form}
    return render(request, "cards/groupcard_update.html", context=context)


def groupcard_delete(request, pk):
    card = Groupcard.objects.get(pk=pk)
    card.delete()
    return redirect("cards:index")



def group_detail(request, pk):
    groupcards = Groupcard.objects.get(pk=pk)
    context = {
        "cards": groupcards,
        "comments": groupcards.groupcomment_set.all(),
    }

    return render(request, "cards/group_detail.html", context)


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
        card = Groupcard.objects.get(pk=pk)
        comment_form = GroupCommentForm(request.POST, request.FILES)
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
            url = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type": "refresh_token",
                "client_id": os.getenv("KAKAO_ID"),
                "refresh_token": card.user.refresh_token,
                "client_secret": os.getenv("KAKAO_SECRET"),
            }
            response = requests.post(url, data=data).json()
            url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
            access_token = response["access_token"]
            headers = {"Authorization": "Bearer " + access_token}
            data = {
                "template_object": json.dumps(
                    {
                        "object_type": "text",
                        "text": request.user.nickname + "님이 트리에 글을 남겨주셨어요.",
                        "link": {"web_url": "http://localhost:8000/cards/" + str(pk)},
                    }
                )
            }
            response = requests.post(url, headers=headers, data=data)
            return redirect("cards:indiv_detail", pk)
    else:
        comment_form = GroupCommentForm()
    context = {"comment_form": comment_form}

    return render(request, "cards/comment_create.html", context)


def gcomment_create(request, pk):
    groupcard = Groupcard.objects.get(pk=pk)
    comment_form = GroupCommentForm(request.POST, request.FILES)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.groupcard = groupcard
        comment.ribbons = request.POST["choice_ribbon"]
        comment.save()
        temp = ""
        for i in str(comment.pk):
            temp += dic[i]
        comment.id_text = temp
        comment.save()
        return redirect("cards:group_detail", pk)
    else:
        comment_form = GroupCommentForm()
    context = {"comment_form": comment_form}

    return render(request, "cards/comment_create.html", context)


def gcomments_delete(request, cards_pk, comment_pk):
    comment = Groupcomment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("cards:group_detail", cards_pk)
