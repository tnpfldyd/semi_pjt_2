from django import forms
from .models import Groupcard, Comment, Groupcomment


class CardForm(forms.ModelForm):
    class Meta:
        model = Groupcard
        fields = ["title", "content", "is_private"]
        labels = {
            "is_private": "Private",
        }


class GroupCardForm(forms.ModelForm):
    class Meta:
        model = Groupcard
        fields = ["title", "content", "is_private"]
        labels = {
            "is_private": "Private",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]


class GroupCommentForm(forms.ModelForm):
    class Meta:
        model = Groupcomment
        fields = [
            "content",
        ]
