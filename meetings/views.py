from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting
from .forms import MeetingForm, CommentForm
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(request):
    meetings = Meeting.objects.order_by("-pk")
    meetings_all = Meeting.objects.all()
    # 모임이 몇개 개설됐는지
    meetings_count = Meeting.objects.all().count()

    # 지역별
    meetings_local = meetings_all
    meetings_local_name = "모든지역"
    meetings_local_list = ["노원구", "송파구"]

    nw = "노원구"
    sp = "송파구"

    at_all = "모두보기"
    paginator = Paginator(meetings, 4)
    page_number = request.GET.get("local") 
    page_obj = paginator.get_page(page_number) 

    if request.POST.get("reset"):
      return redirect('meetings:index')

    if request.GET.get('local') and nw in request.GET.get('local'):

      meetings_local = Meeting.objects.filter(location__contains=nw).order_by("-pk")
      meetings_local_name = nw
      # 페이지네이션
      paginator = Paginator(meetings_local, 4)
      page_number = request.GET.get("local") # key 값이 local, value 값이 노원구 
      page_number = page_number.strip(nw) # 노원구2 에서 노원구를 제거
      page_obj = paginator.get_page(page_number) # 숫자만 받음
      
      context = {
        "nw": nw,
        "meetings": meetings,
        "page_obj": page_obj,
        "meetings_local": meetings_local,
        "meetings_local_name": meetings_local_name,
        "meetings_count": meetings_count,
        "meetings_local_list": meetings_local_list,
      }

      return render(request, 'meetings/index.html', context)

    elif request.GET.get('local') and sp in request.GET.get('local'):
      meetings_local = Meeting.objects.filter(location__contains=sp).order_by("-pk")
      meetings_local_name = sp
      # 페이지네이션
      paginator = Paginator(meetings_local, 4)
      page_number = request.GET.get("local")  
      page_number = page_number.strip(sp) 
      page_obj = paginator.get_page(page_number)

      context = {
        "sp": sp,
        "meetings": meetings,
        "page_obj": page_obj,
        "meetings_local": meetings_local,
        "meetings_local_name": meetings_local_name,
        "meetings_count": meetings_count,
        "meetings_local_list": meetings_local_list,
      }

      return render(request, 'meetings/index.html', context)

    else:

      context = {
          "at_all": at_all,
          "meetings": meetings,
          "page_obj": page_obj,
          "meetings_local": meetings_local,
          "meetings_local_name": meetings_local_name,
          "meetings_count": meetings_count,
          "meetings_local_list": meetings_local_list,
      }
      return render(request, "meetings/index.html", context)


dic = {'0':'zero', '1':'one', '2':'two', '3':'three', '4':'four', '5':'five', '6':'six', '7':'seven', '8':'eight', '9':'nine'}

def create(request):
    if request.method == "POST":
        meeting_form = MeetingForm(request.POST, request.FILES)
        if meeting_form.is_valid():
            meeting = meeting_form.save(commit=False)
            meeting.user = request.user

            meeting.save()
            temp = ''
            for i in str(meeting.pk):
                temp += dic[i]
            meeting.text = temp
            meeting.save()
            return redirect("meetings:index")
    else:
        meeting_form = MeetingForm()
    
    context = {
        "meeting_form": meeting_form,
    }

    return render(request, "meetings/create.html", context)



def detail(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    comments = meeting.comment_set.all()
    form = CommentForm()

    context = {
        "meeting": meeting,
        "comments": comments,
        "commentform": form,
    }

    if request.POST.get('password') == meeting.password:
      print("로직")
      return render(request, "meetings/detail.html", context)
    
    else:
      return redirect("meetings:index")


def update(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    if request.user == meeting.user:
        if request.method == "POST":
            meeting_form = MeetingForm(request.POST, request.FILES, instance=meeting)
            if meeting_form.is_valid():
                meeting_form.save()
                return redirect("meetings:detail", meeting.pk)
        else:
            meeting_form = MeetingForm(instance=meeting)
        context = {
            "meeting_form": meeting_form,
        }
        return render(request, "meetings/update.html", context)
    else:
        return redirect("meetings:detail", meeting.pk)


def delete(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    if request.user == meeting.user:
        meeting.delete()
        return redirect("meetings:index")


def comment_create(request, meeting_pk):
    meeting_data = Meeting.objects.get(pk=meeting_pk)
    print("ddd")

    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        print("여기")
        if form.is_valid():
            print("여긴되나?")
            comment = form.save(commit=False)
            comment.meeting = meeting_data
            comment.user = request.user
            comment.save()

        return redirect('meetings:detail', meeting_pk)
    else:
        return redirect("accounts:login")

def comment_delete(request, meeting_pk, comment_pk):
    meeting_data = Meeting.objects.get(pk=meeting_pk)
    comment_data = meeting_data.comment_set.get(pk=comment_pk)

    if request.user == comment_data.user:
        comment_data.delete()
    
    return redirect("meetings:detail", meeting_pk)