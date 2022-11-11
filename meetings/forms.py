from django import forms
from .models import Meeting, Comment

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            "title",
            "content",
            "image",
            "password",
            "location",
        ]

        labels = {
            "title": "제목",
            "content": "내용",
            "image": "이미지",
            "password": "비밀번호",
            "location": "지역"
        }

        help_texts = {
            "title": '이름을 입력해 주세요.',
            "content": "내용을 입력해 주세요.",
            "image": "이미지를 추가해 주세요.",
            "password": "비밀번호를 추가해 주세요.",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]