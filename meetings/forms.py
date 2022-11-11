from django import forms
from .models import Meeting, Comment

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            "title",
            "content",
            "image",
            "location",
            "password",
            "location",
        ]

        labels = {
            "title": "제목",
            "content": "내용",
            "image": "이미지",
            "location": "지역",
            "password": "비밀번호",
            "location": "지역"
        }

        help_texts = {
            "image": "이미지를 추가해 주세요.",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs = {
            "placeholder": "제목을 입력해 주세요.",
        }
        self.fields["password"].widget.attrs = {
            "placeholder": "4자리 비밀번호를 입력해 주세요.",
        }
        self.fields["content"].widget.attrs = {
            "placeholder": "내용을 입력해 주세요.",
        }
        self.fields["location"].help_text = None

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]