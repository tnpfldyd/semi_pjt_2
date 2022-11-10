from django.shortcuts import render, redirect
from .models import Meeting
from .forms import MeetingForm, CommentForm
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(request):
    meetings = Meeting.objects.order_by("-pk")
    
    # 페이지네이션
    paginator = Paginator(meetings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # 

    # 지역별
    meetings_local = ""
    meetings_local_name = ""
    meetings_local_list = ["강남구","서초구","강동구","성동구", "노원구", "송파구", "용산구",]

    if request.POST.get('노원구'):
      meetings_local = Meeting.objects.filter(location__contains="노원구")
      meetings_local_name = "노원구"
    elif request.POST.get('송파구'):
      meetings_local = Meeting.objects.filter(location__contains="송파구")
      meetings_local_name = "송파구"
    elif request.POST.get('reset'):
      meetings_local = Meeting.objects.order_by('-pk')

    # 모임이 몇개 개설됐는지
    meetings_count = Meeting.objects.all().count()

    context = {
        "meetings": meetings,
        "page_obj": page_obj,
        "meetings_local": meetings_local,
        "meetings_local_name": meetings_local_name,
        "meetings_count": meetings_count,
        "meetings_local_list": meetings_local_list,
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

def update(request, meeting_pk):
    meeting = Meeting.objects.get(pk=meeting_pk)
    if request.user == meeting.user:
        if request.method == "POST":
            password = request.POST.get('password', '') # 비밀번호 값이 있으면 해당 값을 가져오고, 없으면 공백으로 가져옴
            meeting_form = MeetingForm(request.POST, request.FILES, instance=meeting)
            if meeting_form.is_valid() and password == meeting.password: # 유효성 체크 및 비밀번호 검증
                meeting_form.save()
                return redirect("meetings:detail", meeting_pk)
        else:
            meeting_form = MeetingForm(instance=meeting)
            meeting_form.password = ""

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
    else:
        messages.warning(request, "작성자만 삭제할 수 있습니다.")
        return redirect('meetings:index')


