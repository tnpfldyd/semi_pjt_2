from .models import *
from django import forms


class VocieForm(forms.ModelForm):
    class Meta:
        model = Vocie
        fields = (
            "title",
            "content",
            "image",
        )
        labels = {
            "title": "문의 제목",
            "content": "문의 내용",
            "image": "참조 이미지(선택)",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            "content",
        }
        labels = {
            "content": "답변 내용",
        }
