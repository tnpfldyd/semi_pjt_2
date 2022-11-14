from django.shortcuts import render

# Create your views here.
import os, urllib.request, urllib.parse, requests


def index(request):
    if request.GET.get("keyword"):
        keyword = request.GET.get("keyword")
    else:
        keyword = "크리스마스 트리"
    client_id = os.getenv("NAVER_ID")
    client_secret = os.getenv("NAVER_SECRET")
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/shop.json?query=" + encText

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "display": 20,
        "start": 1,
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i in response["items"]:
        i["title"] = i["title"].replace("<b>", "")
        i["title"] = i["title"].replace("</b>", "")
    return render(request, "shoppings/index.html", {"items": response["items"]})


def search(request, num):
    if request.GET.get("keyword"):
        keyword = request.GET.get("keyword")
    else:
        keyword = "크리스마스 용품"
    client_id = os.getenv("NAVER_ID")
    client_secret = os.getenv("NAVER_SECRET")
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/shop.json?query=" + encText

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "display": 20,
        "start": ((num - 1) * 20) + 1,
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i in response["items"]:
        i["title"] = i["title"].replace("<b>", "")
        i["title"] = i["title"].replace("</b>", "")
    return render(request, "shoppings/search.html", {"items": response["items"]})
