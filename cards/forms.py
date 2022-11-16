from django import forms
from .models import *


class GroupCardForm(forms.ModelForm):
    class Meta:
        model = Groupcard
        fields = ["title", "content", "is_private"]
        labels = {
            "is_private": "Private",
        }


class UserCardForm(forms.ModelForm):
    class Meta:
        model = UserCard
        fields = ["title", "content"]
        labels = {
            "title": "",
            "content": "",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "제목을 입력해주세요.",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "내용을 입력해주세요.",
                    "cols": "40",
                    "rows": "10",
                }
            ),
        }


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = [
            "content",
        ]


class GroupCommentForm(forms.ModelForm):
    class Meta:
        model = Groupcomment
        fields = [
            "content",
        ]
