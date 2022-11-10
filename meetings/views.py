from django.shortcuts import render, redirect
from .models import Meeting
from .forms import MeetingForm, CommentForm

# Create your views here.

def index(request):
    meetings = Meeting.objects.order_by("-pk")
    context = {
        "meetings":meetings,
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
            meeting_form = MeetingForm(request.POST, request.FILES, instance=meeting)
            if meeting_form.is_valid():
                meeting_form.save()
                return redirect("meetings:detail", meeting_pk)
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


