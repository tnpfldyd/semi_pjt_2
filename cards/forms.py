from django import forms
from .models import *


class GroupCardForm(forms.ModelForm):
    class Meta:
        model = Groupcard
        fields = ["title", "content", "is_private"]
        labels = {"title": "", "content": "", "is_private": "비공개"}
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
        labels = {
            "content": "",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "메세지 내용을 입력해주세요.",
                }
            ),
        }


class GroupCommentForm(forms.ModelForm):
    class Meta:
        model = Groupcomment
        fields = [
            "content",
        ]
        labels = {
            "content": "",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "메세지 내용을 입력해주세요.",
                }
            ),
        }
