from django.shortcuts import render, redirect

from .forms import *
from .models import *

import requests, os, json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here.


@login_required
def index(request):
    groupcards = Groupcard.objects.order_by("-pk")
    user = get_user_model().objects.get(pk=request.user.pk)
    context = {"groupcards": groupcards, "user": user}
    return render(request, "cards/index.html", context)


# 개인카드 생성, 수정, 삭제, 디테일


@login_required
def usercard_create(request):
    if request.method == "POST":
        form = UserCardForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.userdeco = request.POST["userdeco"]
            temp.chimneys = request.POST["choice_chim"]
            temp.save()
            return redirect("accounts:profile", request.user.pk)
    else:
        form = UserCardForm()
    context = {
        "form": form,
    }
    return render(request, "cards/usercard_create.html", context)


def usercard_detail(request, pk):
    # cards = UserCard.objects.get(user=request.user.pk)
    cards = UserCard.objects.get(pk=pk)
    comments = cards.usercomment_set.all()
    if request.user == cards.user:
        new_comments = cards.usercomment_set.filter(read=False)
        for comment in new_comments:
            comment.read = True
            comment.save()
        request.user.notice_tree = True
        request.user.save()
    context = {
        "cards": cards,
        "comments": comments,
    }
    return render(request, "cards/usercard_detail.html", context)


def usercard_update(request, pk):
    cards = UserCard.objects.get(user=request.user)
    if request.method == "POST":
        form = UserCardForm(request.POST, instance=cards)
        if form.is_valid():
            if form.is_valid():
                temp = form.save(commit=False)
                temp.user = request.user
                # 라디오 버튼 'name'='id'로 들어옴
                # name==choice, id=1,2,3으로 설정
                temp.userdeco = request.POST["userdeco"]
                temp.chimneys = request.POST["choice_chim"]
                temp.save()
                return redirect("cards:usercard_detail", cards.pk)
    else:
        form = UserCardForm(instance=cards)
    context = {"form": form}
    return render(request, "cards/usercard_update.html", context=context)


def usercard_delete(request):
    card = UserCard.objects.get(user_id=request.user.pk)
    card.delete()
    return redirect("accounts:profile", request.user.pk)


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
            if card.user.tree_notice:
                card.user.notice_tree = False
                card.user.save()
            temp = ""
            for i in str(comment.pk):
                temp += dic[i]
            comment.id_text = temp
            comment.save()
            if card.user.refresh_token:
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
            return redirect("cards:usercard_detail", pk)
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


def card_delete(request):
    card = Groupcard.objects.get(user_id=request.user.pk, is_indiv=1)


def groupcard_update(request, pk):
    cards = Groupcard.objects.get(pk=pk)
    if request.method == "POST":
        form = GroupCardForm(request.POST, instance=cards)
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
    request.user.card_created = 0
    request.user.save()
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


def gcomment_create(request, pk):
    if request.method == "POST":
        card = Groupcard.objects.get(pk=pk)
        comment_form = GroupCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.groupcard = card
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
            return redirect("cards:group_detail", card.pk)
    else:
        comment_form = GroupCommentForm()
    context = {"comment_form": comment_form}

    return render(request, "cards/gcomment_create.html", context)
