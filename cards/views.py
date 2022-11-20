from django.shortcuts import render, redirect

from .forms import *
from .models import *

import requests, os, json, re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


@login_required
def index(request):
    groupcards = Groupcard.objects.order_by("-pk")
    popularity = UserCard.objects.annotate(follow=Count("user__followers")).order_by(
        "-follow"
    )[:5]
    random_user = UserCard.objects.order_by("?")[:5]
    user = get_user_model().objects.get(pk=request.user.pk)
    # pop_user = UserCard.
    print(popularity, random_user)
    context = {
        "groupcards": groupcards,
        "user": user,
        "random_user": random_user,
        "popular": popularity,
    }
    return render(request, "cards/index.html", context)


# 개인카드 생성, 수정, 삭제, 디테일


@login_required
def usercard_create(request):
    if request.method == "POST":
        form = UserCardForm(request.POST)
        if form.is_valid():
            try:
                temp = form.save(commit=False)
                # 라디오 버튼 'name'='id'로 들어옴
                # name==choice, id=1,2,3으로 설정
                temp.user = request.user
                temp.userdeco = request.POST["userdeco"]
                temp.chimneys = request.POST["choice_chim"]
                temp.save()
                return redirect("cards:usercard_create2")
            except:
                cards = UserCard.objects.get(user=request.user)
                form = UserCardForm(request.POST, instance=cards)
                if cards.userdeco and cards.chimneys:
                    cards.user = request.user
                    cards.userdeco = request.POST["userdeco"]
                    cards.chimneys = request.POST["choice_chim"]
                    cards.save()
                    return redirect("cards:usercard_create2")
    else:
        form = UserCardForm()
    context = {
        "form": form,
    }
    return render(request, "cards/usercard_create.html", context)


@login_required
def usercard_create2(request):
    cards = UserCard.objects.get(user=request.user)
    if request.method == "POST":
        form = UserCardForm(request.POST, instance=cards)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.userdeco = cards.userdeco
            temp.chimneys = cards.chimneys
            temp.save()
            return redirect("accounts:profile", request.user.pk)
    else:
        form = UserCardForm(instance=cards)
    context = {
        "form": form,
        "cards": cards,
    }
    return render(request, "cards/usercard_create2.html", context=context)


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
        "cl": list(range(1, comments.count() // 40 + 2)),
    }
    return render(request, "cards/usercard_detail.html", context)


def usercard_update(request, pk):
    cards = UserCard.objects.get(user=request.user)
    if request.method == "POST":
        form = UserCardForm(request.POST, instance=cards)
        if form.is_valid():
            try:
                temp = form.save(commit=False)
                temp.user = request.user
                # 라디오 버튼 'name'='id'로 들어옴
                # name==choice, id=1,2,3으로 설정
                temp.userdeco = request.POST["userdeco"]
                temp.chimneys = request.POST["choice_chim"]
                temp.save()
                return redirect("cards:usercard_update2", cards.pk)
            except:
                messages.error(request, "벽난로와 본인의 아이덴티티 장식을 반드시 선택해주세요.😥")
                return redirect("cards:usercard_update", cards.pk)
    else:
        form = UserCardForm(instance=cards)
    context = {"form": form}
    return render(request, "cards/usercard_update.html", context=context)


def usercard_update2(request, pk):
    cards = UserCard.objects.get(user=request.user)
    if request.method == "POST":
        form = UserCardForm(request.POST, instance=cards)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.userdeco = cards.userdeco
            temp.chimneys = cards.chimneys
            temp.save()
            return redirect("cards:usercard_detail", cards.pk)
    else:
        form = UserCardForm(instance=cards)
    context = {
        "form": form,
        "cards": cards,
    }
    return render(request, "cards/usercard_update2.html", context=context)


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
        comment_form = UserCommentForm(request.POST)
        if comment_form.is_valid():
            try:
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.usercard = card
                comment.socks = request.POST["socks"]
                comment.save()
                if card.user.tree_notice:
                    card.user.notice_tree = False
                    card.user.save()
                temp = ""
                for i in str(comment.pk):
                    temp += dic[i]
                comment.id_text = temp
                comment.save()
                # if card.user.refresh_token:
                #     url = "https://kauth.kakao.com/oauth/token"
                #     data = {
                #         "grant_type": "refresh_token",
                #         "client_id": os.getenv("KAKAO_ID"),
                #         "refresh_token": card.user.refresh_token,
                #         "client_secret": os.getenv("KAKAO_SECRET"),
                #     }
                #     response = requests.post(url, data=data).json()
                #     url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
                #     access_token = response["access_token"]
                #     headers = {"Authorization": "Bearer " + access_token}
                #     data = {
                #         "template_object": json.dumps(
                #             {
                #                 "object_type": "text",
                #                 "text": request.user.nickname + "님이 트리에 글을 남겨주셨어요.",
                #                 "link": {
                #                     "web_url": "http://localhost:8000/cards/detail/usercard/"
                #                     + str(pk)
                #                     + "/"
                #                 },
                #             }
                #         )
                #     }
                #     response = requests.post(url, headers=headers, data=data)
                return redirect("cards:usercard_comment2", comment.pk)
            except:
                messages.error(request, "메세지의 장식을 반드시 선택해주세요.😥")
                return redirect("cards:usercard_comment", pk)

    else:
        comment_form = UserCommentForm()
    context = {"comment_form": comment_form}

    return render(request, "cards/usercard_comment.html", context)


def usercard_comment2(request, pk):
    comment = UserComment.objects.get(pk=pk)
    card = comment.usercard
    if request.method == "POST":
        comment_form = UserCommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comments = comment_form.save(commit=False)
            comments.user = request.user
            comments.usercard = card
            comments.socks = comment.socks
            comments.save()
            if card.user.tree_notice:
                card.user.notice_tree = False
                card.user.save()
            temp = ""
            for i in str(comment.pk):
                temp += dic[i]
            comments.id_text = temp
            comments.save()
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
                            "link": {
                                "web_url": "http://localhost:8000/cards/detail/usercard/"
                                + str(pk)
                                + "/"
                            },
                        }
                    )
                }
                response = requests.post(url, headers=headers, data=data)
            return redirect("cards:usercard_detail", card.pk)
    else:
        comment_form = UserCommentForm()
    context = {
        "comment_form": comment_form,
        "comment": comment,
    }

    return render(request, "cards/usercard_comment2.html", context)


# 그룹카드 생성, 수정, 삭제, 디테일
@login_required
def group_create(request):
    if request.method == "POST":
        form = GroupCardForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.groupdeco = request.POST["userdeco"]
            temp.chimneys = request.POST["choice_chim"]
            temp.save()
            return redirect("cards:group_create2")
    else:
        form = GroupCardForm()
    context = {
        "form": form,
    }
    return render(request, "cards/group_create.html", context)


@login_required
def group_create2(request):
    card = Groupcard.objects.get(user=request.user)
    if request.method == "POST":
        form = GroupCardForm(request.POST, instance=card)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.groupdeco = card.groupdeco
            temp.chimneys = card.chimneys
            temp.save()
            return redirect("cards:index")
    else:
        form = GroupCardForm(instnace=card)
    context = {
        "form": form,
    }
    return render(request, "cards/group_create2.html", context)


def group_detail(request, pk):
    groupcards = Groupcard.objects.get(pk=pk)
    context = {
        "groupcards": groupcards,
        "comments": groupcards.groupcomment_set.all(),
    }

    return render(request, "cards/group_detail.html", context)


def groupcard_update(request, pk):
    cards = Groupcard.objects.get(pk=pk)
    if request.method == "POST":
        form = GroupCardForm(request.POST, instance=cards)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            # 라디오 버튼 'name'='id'로 들어옴
            # name==choice, id=1,2,3으로 설정
            temp.groupdeco = request.POST["groupdeco"]
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


def gcomment_create(request, pk):
    if request.method == "POST":
        card = Groupcard.objects.get(pk=pk)
        comment_form = GroupCommentForm(request.POST)
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
                        "text": request.user.nickname + "님이 벽난로에 글을 남겨주셨어요.",
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


def search(request):
    all_data = Groupcard.objects.filter(is_private=0).order_by("-pk")
    search = request.GET.get("search")
    paginator = Paginator(all_data, 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    print(request.GET)
    if search:
        search_list = all_data.filter(Q(title__icontains=search))
        paginator = Paginator(search_list, 6)
        page_obj = paginator.get_page(request.GET.get("page"))
        context = {
            "search": search,
            "search_list": search_list,
            "question_list": page_obj,
        }
    else:
        context = {
            "search": search,
            "search_list": all_data,
            "question_list": page_obj,
        }

    return render(request, "cards/search.html", context)
