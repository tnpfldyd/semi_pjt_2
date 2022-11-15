from django import forms
from .models import Groupcard, Comment, Groupcomment, UserCard, UserComment


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
