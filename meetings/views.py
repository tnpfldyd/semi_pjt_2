from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting
from .forms import MeetingForm, CommentForm, UpdateMeetingForm
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(request):
    meetings = Meeting.objects.order_by("-pk")
    
    # 페이지네이션
    Paginator = Paginator(meetings, 10)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(page_number)
    # 

    # 지역별
    meetings_local = ""

    if request.POST.get('노원구'):
      meetings_local = Meeting.objects.filter(location__contains="노원구")
    elif request.POST.get('송파구'):
      meetings_local = Meeting.objects.filter(location__contains="송파구")
    elif request.POST.get('reset'):
      meetings_local = Meeting.objects.order_by('-pk')

    # 모임이 몇개 개설됐는지
    meetings_count = Meeting.objects.all().count()

    context = {
        "meetings": meetings,
        "page_obj": page_obj,
        "meetings_local": meetings_local,
        "meetings_count": meetings_count,
    }
    return render(request, "meetings/index.html", context)


def create(request):
    if request.method == "POST":
        meeting_form = MeetingForm(request.POST, request.FILES)
        if meeting_form.is_valid():
            meeting = meeting_form.save(commit=False)
            meeting.user = request.user
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
    comment = meeting.comment_set.all()
    form = CommentForm()

    context = {
        "meeting": meeting,
        "comment": comment,
        "commentform": form,
    }

    return render(request, "meetings/detail.html", context)


def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        meeting = get_object_or_404(Meeting, pk=request.POST.get('id'))
        password = request.POST.get('password', '') # 비밀번호 값이 있으면 해당 값을 가져오고 없으면 공백으로 가져옴
        form = UpdateMeetingForm(request.POST, instance=meeting)
        if form.is_valid() and password == meeting.password: # 유효성 체크 및 비밀번호 검증
            meeting = form.save()
    elif request.method == 'GET':
        meeting = get_object_or_404(Meeting, pk=request.GET.get('id'))
        form = MeetingForm(instance=meeting)
        form.password = ""
        context = {
            "form":form,
        }
        return render(request, 'meetings/update.html', context)
    return redirect('meetings:detail')

def delete(request, meeting_pk):
    meeting = get_object_or_404(Meeting, pk=meeting_pk)
    if request.method == 'POST' and 'password' in request.POST:
        if meeting.password == request.POST.get('password'):
            meeting.delete()
            return redirect('meetings:index')

def comment_create(request, meeting_pk):
    meeting_data = Meeting.objects.get(pk=meeting_pk)

    if request.user.is_authenticated:
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.meeting = meeting_data
            comment.user = request.user
            comment.save()

        return redirect('meetings:detail', meeting_data.pk)
    else:
        return redirect("accounts:login")

def comment_delete(request, meeting_pk, comment_pk):
    meeting_data = Meeting.objects.get(pk=meeting_pk)
    comment_data = meeting_data.comment_set.get(pk=comment_pk)

    if request.user == comment_data.user:
        comment_data.delete()
    
    return redirect("meetings:detail", meeting_data.pk)