from django.shortcuts import render

# Create your views here.
import os, urllib.request, urllib.parse, requests
from django.http import JsonResponse


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
        "display": 100,
        "start": 1,
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i in response["items"]:
        i["title"] = i["title"].replace("<b>", "")
        i["title"] = i["title"].replace("</b>", "")

    return render(request, "shoppings/index.html", {"items": response["items"]})


def search(request):
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
        "display": 100,
        "start": 1,
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i in response["items"]:
        i["title"] = i["title"].replace("<b>", "")
        i["title"] = i["title"].replace("</b>", "")
    context = {
        "items": response["items"],
        "keyword": keyword,
    }
    print(response)
    return render(request, "shoppings/search.html", context)


def ssort(request, string):
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
        "display": 100,
        "start": 1,
        "sort": string,
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i in response["items"]:
        i["title"] = i["title"].replace("<b>", "")
        i["title"] = i["title"].replace("</b>", "")
    return JsonResponse(response)
