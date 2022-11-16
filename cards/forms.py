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
